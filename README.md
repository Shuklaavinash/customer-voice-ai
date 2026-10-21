# Customer Voice AI — File Q&A Website

Upload CSV, Excel, PDF, TXT, or Markdown files, ask a question, and view relevant evidence retrieved from the uploaded content.

## Run locally
Install Python 3.10+ and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy online
https://customer-voice-ai-ehxvmnaysbkwvcatw6vqvz.streamlit.app/

## Features
- CSV and Excel table upload and preview
- PDF, TXT, and Markdown text extraction
- Semantic search across rows or document sections
- Evidence snippets with similarity scores
- Basic numeric overview for tabular data
- CSV download

## Limitations
This starter version retrieves relevant content and assembles a short extractive answer. It is not yet a full generative AI chatbot. Scanned PDFs need OCR. Very large files may need more resources. Avoid uploading confidential files to a public deployment.
