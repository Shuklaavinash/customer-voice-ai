# Customer Voice AI – Customer Feedback Analysis & Intelligence System

## Overview

Customer Voice AI is a Machine Learning and NLP-based application designed to help businesses understand customer feedback, analyze customer sentiment, and discover meaningful insights from customer reviews and reports.

The project uses sentiment analysis and semantic search techniques to identify positive and negative feedback, retrieve relevant customer reviews, summarize feedback patterns, and help users explore customer opinions through an interactive Streamlit dashboard.

The long-term goal is to build a user-friendly AI-powered website where customers and business teams can upload their own analysis files or reports, ask questions about their data, and receive useful insights.

Live Website: https://customer-voice-ai-ehxvmnaysbkwvcatw6vqvz.streamlit.app/

## Features

* Customer Review and Feedback Analysis
* Sentiment Analysis (Positive and Negative)
* Sentiment Confidence Scores
* Semantic Search for Relevant Reviews
* AI-Based Review Retrieval
* Customer Feedback Summary
* Common Words and Feedback Pattern Analysis
* Interactive Data Visualizations
* CSV Export of Analysis Results
* Streamlit-Based Web Interface
* Support for Uploaded Customer Feedback Data 

## Machine Learning Techniques

* Natural Language Processing (NLP)
* DistilBERT-Based Sentiment Classification
* Sentence Transformers for Text Embeddings
* Semantic Similarity Search
* FAISS for Efficient Vector Search
* Text Preprocessing and Analysis
* Retrieval-Based Question Answering

## Tech Stack

### Frontend and Web Application

* Streamlit

### Machine Learning and NLP

* Hugging Face Transformers
* DistilBERT
* Sentence Transformers
* `all-MiniLM-L6-v2`
* FAISS

### Data Processing and Visualization

* Pandas
* NumPy
* Matplotlib
* Seaborn

### Programming Language

* Python

## Project Structure

```text
Customer-Voice-AI/
│
├── app.py
├── requirements.txt
├── README.md
└── Customer_Voice_AI.ipynb
```

## How It Works

1. **Input Data:** Customer reviews or feedback data are provided to the application.
2. **Sentiment Analysis:** A pretrained DistilBERT model classifies reviews as positive or negative and provides confidence scores.
3. **Text Embeddings:** Sentence Transformers convert review text into numerical vector representations.
4. **Semantic Search:** FAISS can be used to retrieve reviews that are semantically similar to a user's query.
5. **Insight Generation:** The application helps users explore sentiment distribution, relevant reviews, and common feedback patterns.
6. **Visualization:** Results are presented through an interactive dashboard for easier interpretation.

## Installation

```bash
git clone <repository-url>
cd Customer-Voice-AI

python -m venv venv

# Windows
venv\Scripts\activate

python -m pip install -r requirements.txt

python -m streamlit run app.py
```

## Future Improvements

* Integrate the original Colab ML/NLP pipeline directly into the website
* Support customer uploads in CSV, Excel, PDF, and TXT formats
* Add natural-language question answering over uploaded reports
* Implement a complete Retrieval-Augmented Generation (RAG) pipeline
* Generate automatic summaries of customer feedback
* Add topic detection and complaint categorization
* Support multilingual sentiment analysis
* Improve performance for large datasets
* Add secure file handling and user authentication
* Deploy a scalable, production-ready version

## Project Objective

The objective of Customer Voice AI is to transform unstructured customer feedback into actionable insights using Machine Learning, NLP, and semantic search. It demonstrates practical applications of AI in customer experience analysis, feedback management, and data-driven decision-making.
