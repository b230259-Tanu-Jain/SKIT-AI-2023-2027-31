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

Under development. As of 15 November 2026, the repository contains a working
resume PDF parser with contact, skill, education, experience, project, and
certification extraction; a saved TF-IDF/LinearSVC job-category model and
posting similarity index; and an initial, interpretable skill-gap comparison
against the role-skill dataset. The saved model metrics are documented, but
its original postings CSV is not checked in, so retraining requires supplying
that dataset separately. The local resume and skill-gap CLI flows, the saved
matcher artifact, and the model training path have automated tests.

Vanshika's Form 2 career-role matching milestone ended 10 November 2026. The
repository has a TF-IDF/LinearSVC category predictor and posting similarity
retriever; end-to-end validation against labelled resume/job matches and UI/API
integration remain open. Her skill-gap sprint runs 1 November-5 December 2026.
The skill-gap CLI checks the selected role's exact skill phrases against the
resume text in addition to the general extractor vocabulary. This improves
coverage while remaining transparent; paraphrases and scanned PDFs still need
review/OCR. Career-readiness (scheduled 6-20 December) and final integration
(scheduled 21 December-31 March) are future milestones, not complete as of
today.

### Run resume analysis

```bash
python -m pip install -r features/resume_analysis/requirements.txt
python -m features.resume_analysis.main path/to/resume.pdf
```

### Run skill-gap analysis

```bash
python -m features.skill_gap.main path/to/resume.pdf --role "Sr Human Resource Generalist"
```

### Get job recommendations from a PDF resume

```bash
python -m features.resume_analysis.job_matcher recommend-resume \
  --resume path/to/resume.pdf \
  --limit 5
```

Use a role name listed in `data/raw/job_role_skills.csv`. For model retraining
and evaluation instructions, see
[`features/resume_analysis/MODEL_TRAINING_GUIDE.md`](features/resume_analysis/MODEL_TRAINING_GUIDE.md).

### Verify Vanshika's current modules

From the project root, run:

```bash
python3 -m unittest discover -s features/resume_analysis/tests -v
```

This exercises resume extraction, skill-gap PDF-to-JSON output, temporary
model training, and loading the checked-in matcher artifact.
