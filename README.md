# Customer Voice AI — File Q&A Website

Upload CSV, Excel, PDF, TXT, or Markdown files, ask a question, and view relevant evidence retrieved from the uploaded content.

## Run locally
Install Python 3.10+ and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy online
1. Upload `app.py`, `requirements.txt`, and this README to a GitHub repository.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Create an app, select your repository, and set `app.py` as the main file.
4. Deploy and wait for dependencies and the embedding model to download.

## Features
- CSV and Excel table upload and preview
- PDF, TXT, and Markdown text extraction
- Semantic search across rows or document sections
- Evidence snippets with similarity scores
- Basic numeric overview for tabular data
- CSV download

## Limitations
This starter version retrieves relevant content and assembles a short extractive answer. It is not yet a full generative AI chatbot. Scanned PDFs need OCR. Very large files may need more resources. Avoid uploading confidential files to a public deployment.
