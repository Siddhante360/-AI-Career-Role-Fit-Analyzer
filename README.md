# AI Career Role Fit Analyzer

An AI-powered resume evaluation system that predicts compatibility across 30+ technical job roles using NLP and semantic similarity.

## Features

- PDF Resume Parsing (PyMuPDF)
- Semantic Similarity using SentenceTransformer
- Cosine Similarity-based Scoring
- Core & Bonus Skill Matching
- Fuzzy Matching (RapidFuzz)
- Skill Gap Analysis
- Streamlit Interactive Dashboard

## Tech Stack

- Python
- Sentence Transformers
- Scikit-learn
- RapidFuzz
- PyMuPDF
- Streamlit

## Scoring Formula

Final Score =  
0.5 × Semantic Similarity  
+ 0.35 × Core Skill Match  
+ 0.15 × Bonus Skill Match  

## 🚀 How to Run

```bash
pip install -r requirements.txt
python -m streamlit run app.py
