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

Under development. As of 11 November 2026, the repository contains a working
resume PDF parser with contact, skill, education, experience, project, and
certification extraction; a saved TF-IDF/LinearSVC job-category model and
posting similarity index; and an initial, interpretable skill-gap comparison
against the role-skill dataset. The saved model metrics are documented, but
its original postings CSV is not checked in, so retraining requires supplying
that dataset separately.

Vanshika's Form 2 career-role matching milestone ended 10 November 2026. The
repository has a TF-IDF/LinearSVC category predictor and posting similarity
retriever; end-to-end validation against labelled resume/job matches and UI/API
integration remain open. Her skill-gap sprint runs 1 November-5 December 2026.
An initial exact normalized skill comparison is implemented; broader skill
vocabulary coverage, validation, and UI/API integration remain in progress.
Career-readiness and final integration are later scheduled milestones.

### Run resume analysis

```bash
python -m pip install -r features/resume_analysis/requirements.txt
python -m features.resume_analysis.main path/to/resume.pdf
```

### Run skill-gap analysis

```bash
python -m features.skill_gap.main path/to/resume.pdf --role "Sr Human Resource Generalist"
```

Use a role name listed in `data/raw/job_role_skills.csv`. For model retraining
and evaluation instructions, see
[`features/resume_analysis/MODEL_TRAINING_GUIDE.md`](features/resume_analysis/MODEL_TRAINING_GUIDE.md).
