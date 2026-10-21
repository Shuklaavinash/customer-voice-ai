import re
import pandas as pd
import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Customer Voice AI", page_icon="💬", layout="wide")
st.title("💬 Customer Voice AI")
st.caption("Upload a report or data file, ask a question, and explore relevant evidence.")

@st.cache_resource(show_spinner="Loading semantic search model (first run only)...")
def load_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def read_file(file):
    name = file.name.lower()
    if name.endswith(".csv"):
        try:
            return "table", pd.read_csv(file)
        except UnicodeDecodeError:
            file.seek(0)
            return "table", pd.read_csv(file, encoding="latin-1")
    if name.endswith((".xlsx", ".xls")):
        return "table", pd.read_excel(file)
    if name.endswith(".pdf"):
        reader = PdfReader(file)
        text = "\n\n".join(
            f"[Page {i}]\n{page.extract_text() or ''}"
            for i, page in enumerate(reader.pages, start=1)
        )
        return "document", text
    if name.endswith((".txt", ".md")):
        return "document", file.getvalue().decode("utf-8", errors="replace")
    raise ValueError("Unsupported file type.")

def split_text(text, max_chars=900, overlap=120):
    text = re.sub(r"\s+", " ", text).strip()
    chunks, start = [], 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start + int(max_chars * .65), end)
            if boundary > start:
                end = boundary
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return [c for c in chunks if c]

def table_chunks(df):
    chunks = []
    for idx, row in df.iterrows():
        parts = [f"{col}: {value}" for col, value in row.items() if pd.notna(value)]
        if parts:
            chunks.append(f"Row {idx + 1}: " + " | ".join(parts))
    return chunks

def evidence_answer(question, chunks, scores, count=3):
    chosen = [(chunks[i], float(scores[i])) for i in range(min(count, len(chunks)))]
    terms = {w for w in re.findall(r"[a-zA-Z0-9]+", question.lower()) if len(w) > 2}
    candidates = []
    for text, _ in chosen:
        for sentence in re.split(r"(?<=[.!?])\s+|\s+\|\s+", text):
            sentence = sentence.strip()
            if sentence:
                overlap = len(terms & set(re.findall(r"[a-zA-Z0-9]+", sentence.lower())))
                candidates.append((overlap, sentence))
    candidates.sort(key=lambda x: x[0], reverse=True)
    answer, seen = [], set()
    for _, sentence in candidates:
        if sentence.lower() not in seen:
            answer.append(sentence)
            seen.add(sentence.lower())
        if len(answer) >= 3:
            break
    return " ".join(answer) if answer else (chosen[0][0] if chosen else "No relevant evidence found."), chosen

uploaded = st.file_uploader(
    "Upload your file",
    type=["csv", "xlsx", "xls", "pdf", "txt", "md"]
)

if uploaded is None:
    st.info("Upload a CSV, Excel, PDF, TXT, or Markdown file to begin.")
    st.markdown("**Example questions**")
    st.write("- What are the main customer complaints?")
    st.write("- What does the report say about delivery?")
    st.write("- Which rows mention poor product quality?")
    st.write("- What are the average values in this dataset?")
    st.stop()

try:
    kind, content = read_file(uploaded)
except Exception as exc:
    st.error(f"Could not read this file: {exc}")
    st.stop()

if kind == "table":
    df = content
    if df.empty:
        st.warning("The file contains no data rows.")
        st.stop()
    st.success(f"Loaded {uploaded.name}: {len(df):,} rows and {len(df.columns):,} columns.")
    with st.expander("Preview data", expanded=True):
        st.dataframe(df.head(100), use_container_width=True)
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        st.subheader("Quick numeric overview")
        cols = st.columns(min(4, len(numeric.columns)))
        for i, col in enumerate(numeric.columns[:4]):
            cols[i].metric(f"Average · {col}", f"{numeric[col].mean():,.2f}" if numeric[col].notna().any() else "N/A")
        with st.expander("Detailed numeric summary"):
            st.dataframe(numeric.describe().T, use_container_width=True)
    st.download_button("Download data as CSV", df.to_csv(index=False).encode("utf-8"), "uploaded_data.csv", "text/csv")
    if len(df) > 5000:
        st.warning("For this demo, semantic search uses only the first 5,000 rows.")
        df = df.head(5000)
    chunks = table_chunks(df)
else:
    if not content.strip():
        st.error("No readable text found. Scanned PDFs need OCR before upload.")
        st.stop()
    chunks = split_text(content)
    st.success(f"Loaded {uploaded.name}: {len(chunks)} searchable text sections.")
    with st.expander("Preview extracted text"):
        st.text(content[:5000])

if not chunks:
    st.error("No searchable content found in the file.")
    st.stop()

with st.spinner("Preparing searchable content..."):
    model = load_model()
    doc_embeddings = model.encode(chunks, normalize_embeddings=True, show_progress_bar=False)

st.divider()
st.subheader("Ask a question about your file")
question = st.text_input("Your question", placeholder="e.g. What are the main customer complaints?")
top_k = st.slider("Evidence sections to retrieve", 1, 8, 4)

if st.button("Find answer", type="primary", disabled=not question.strip()):
    with st.spinner("Searching your file..."):
        query_embedding = model.encode([question], normalize_embeddings=True)
        scores = cosine_similarity(query_embedding, doc_embeddings)[0]
        ids = scores.argsort()[::-1][:top_k]
        ranked_chunks = [chunks[i] for i in ids]
        ranked_scores = [float(scores[i]) for i in ids]
        answer, evidence = evidence_answer(question, ranked_chunks, ranked_scores, count=min(3, top_k))
    st.markdown("### Answer from your file")
    st.write(answer)
    st.caption("This starter version retrieves relevant content and presents an evidence-based extractive answer; it does not use a generative chatbot model.")
    st.markdown("### Supporting evidence")
    for i, (snippet, score) in enumerate(evidence, start=1):
        with st.expander(f"Evidence {i} · similarity {score:.3f}", expanded=(i == 1)):
            st.write(snippet)

st.divider()
st.caption("Privacy: files are processed by the running app. Do not upload confidential reports to a public deployment unless you have reviewed the hosting provider's privacy settings.")
