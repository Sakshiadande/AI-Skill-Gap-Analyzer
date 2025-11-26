# AI-Powered Skill Gap Analyzer

An AI-driven system that compares candidate resumes with job descriptions to identify skill gaps using NLP and Sentence-BERT.  
The system extracts skills from documents, computes semantic similarity scores, classifies skill gaps (Matched / Weak / Missing), visualizes results using charts, and generates downloadable reports.

## Features
- Resume & Job Description upload (PDF, DOCX, TXT)
- Skill extraction using spaCy and keyword filtering
- Similarity scoring using SBERT (all-MiniLM-L6-v2)
- Gap classification and visualization (Charts & Tables)
- Export report to CSV/XLSX
- Streamlit dashboard

## Tech Stack
| Component | Technology |
|-----------|------------|
| Language | Python |
| NLP | spaCy, Sentence-BERT |
| UI | Streamlit |
| Embeddings | Sentence-transformers |
| Visualization | Matplotlib, Plotly |
| File Parsing | pdfminer, python-docx |
| Export | Pandas, Openpyxl |

## Workflow
1. Upload Resume & JD
2. Extract and clean text
3. Extract skills
4. Generate embeddings
5. Compare similarity
6. Visualize & Export gaps

## Installation
```bash
git clone https://github.com/Sakshiadande/AI-Skill-Gap-Analyzer.git
cd AI-Skill-Gap-Analyzer
pip install -r requirements.txt
streamlit run app.py
