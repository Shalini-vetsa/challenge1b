# 📄 Adobe India Hackathon 2025 – Challenge 1B
Persona-Based Document Summarizer

This project solves Challenge 1B of the Adobe India Hackathon 2025 by implementing a persona-driven intelligent document summarizer. It processes PDFs, ranks sections relevant to a given persona and job, and generates personalized summaries using NLP models.

## 🔍 Problem Statement
Given a set of PDF documents, extract and rank content based on how relevant it is to a specified persona and job description, then summarize the top-ranked sections to generate a personalized document summary.

🧠 Key Features
✅ PDF text extraction via PyMuPDF (fitz)
✅ Smart chunking and section title identification
✅ Persona-relevance ranking using TF-IDF
✅ Natural Language Summarization using DistilBART (from 🤗 Transformers)
✅ Docker support for portability
✅ Outputs structured, explainable JSON results

📁 Folder Structure
project/
│
├── Collection 1/
│   ├── pdfs/                         # Input PDFs
│   ├── challenge1b_input.json        # Persona & job description input
│   └── challenge1b_output.json       # Final output JSON summary
│
├── utils/
│   ├── text_extraction.py           # PDF to text extraction
│   ├── persona_ranking.py           # Relevance scoring (TF-IDF)
│   └── summarizer.py                # Summarizer using DistilBART
│
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker build instructions
└── .dockerignore                    # Files to exclude from Docker context
🛠️ Tech Stack
Component	Tool/Library
Language	Python 3.10
NLP Model	🤗 Transformers (DistilBART: facebook/distilbart-cnn-12-6)
PDF Parsing	PyMuPDF (fitz)
Relevance Scoring	TF-IDF (Scikit-learn, NLTK)
Containerization	Docker

⚙️ Setup & Execution
🔨 Step 1: Build Docker Image
Navigate to the root folder where the Dockerfile is present.
docker build -t adobe_challenge1b .

▶️ Step 2: Run the Docker Container
Run the summarizer and mount your current folder into Docker:
docker run --rm -v "${PWD}:/app" adobe_challenge1b

📁 Output will be generated at:
Collection 1/challenge1b_output.json

🔄 How It Works
Text Extraction
  -- Extracts text from all pages in the PDFs using PyMuPDF.

Section Chunking
  -- Splits text into clean, readable chunks (~300 words) and tries to associate them with nearby titles.

Persona Relevance Ranking
  -- Compares each chunk to the persona and job description using TF-IDF cosine similarity.
  -- Top 5–7 relevant chunks are selected for summarization.

Summarization
  -- Uses facebook/distilbart-cnn-12-6 transformer to summarize selected chunks.
  -- Results include the chunk's original location, relevance score, and summary.

Output Format
Outputs a structured JSON including:
  -- Chunk title
  -- Source PDF filename
  -- Page number(s)
  -- Relevance score
  -- Summarized text

📤 Sample Output Format
[
  {
    "source_file": "file01.pdf",
    "page_range": "2-3",
    "section_title": "Deep Learning Applications",
    "relevance_score": 0.89,
    "summary": "This section discusses real-world applications of deep learning, including healthcare, finance, and natural language processing..."
  },
  {
    "source_file": "file01.pdf",
    "page_range": "4",
    "section_title": "Neural Networks",
    "relevance_score": 0.84,
    "summary": "The neural network architecture is explained with emphasis on forward propagation, backpropagation, and activation functions..."
  }
]