# WorkSphere

## AI-Powered Career Intelligence Platform

WorkSphere is an AI-driven platform that analyzes user resumes,
job-role requirements, company reviews and workplace attributes
to provide personalized career insights.

## Key Features

- Resume Analysis
- Skill Extraction
- Role Matching
- Skill Gap Analysis
- Company Intelligence
- Personalized Company Recommendations
- Company Comparison

## Technology Stack

### Frontend
- React.js
- Figma

### Backend
- Python
- FastAPI

### AI/ML
- NLP
- Scikit-learn
- Sentence-BERT / Transformers

### Database
- MongoDB

## Team

- Tanu Jain — Company Intelligence Module
- Vanshika Choudhary — Resume Intelligence & Skill Gap
- Vaibhav Munot — UI/UX & Frontend

## Project Status

Currently under development.

=======

## Resume Intelligence (Sprint 2)

The Resume Intelligence module now supports text-based PDF resumes. It extracts PDF text with `pypdf`, normalises common PDF artefacts, and returns a starter structured profile with contact details and text-only education, experience, project, and certification sections. Skill extraction is deliberately deferred to its scheduled NLP sprint.

Install the backend dependencies, then run:

```bash
python -m features.resume_analysis.main path/to/resume.pdf
```

## Run from the terminal

Create a virtual environment and install the core Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirement.txt
python run.py --list-roles
```

To analyse a text-based resume PDF, use `python run.py --resume path/to/resume.pdf`.
Scanned PDFs need OCR before they can be processed. Company BERT sentiment analysis is optional and requires `pip install -r backend/requirements-ml.txt`.

To run the React prototype:

```bash
cd frontend
npm install
npm run dev
```
>>>>>>> 806a23b (Updated project features)
