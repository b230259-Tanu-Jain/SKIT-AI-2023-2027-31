# Resume Intelligence - Vanshika Choudhary

## Status as of 4 November 2026

Completed work in this folder:

- PDF resume text extraction and cleaning (PyMuPDF with pypdf fallback).
- NLP-assisted technical skill extraction, plus education, experience, project,
  certification, and basic contact extraction.
- Career category prediction and job-posting similarity retrieval using the
  saved TF-IDF/LinearSVC model. The saved metrics report 1,167 training rows
  and 0.936 macro F1 on a 234-row holdout; the original postings CSV is not in
  this repository, so reproducing the metrics requires obtaining that exact
  permitted dataset.
- Career-role matching is in its Form 2 window through 10 November. Skill-gap
  analysis is scheduled 1 November-5 December and has an initial exact,
  normalized comparison implementation in `features/skill_gap/main.py`.

Run from the project root:

```bash
pip install -r features/resume_analysis/requirements.txt
python -m features.resume_analysis.main path/to/resume.pdf
```

The output is a JSON profile with raw/clean text, contact details, recognised
skills, education, experience, projects, and certifications. The module uses
PyMuPDF for PDF text extraction (with a pypdf fallback), and then applies the
local NLP skill vocabulary plus education and experience extractors.

The runnable command is:

```bash
python -m features.resume_analysis.main path/to/resume.pdf
```

## Job-postings model

The resume-to-job model is trained from the supplied `all_job_post.csv` file.
It classifies resume text into the dataset's career categories and retrieves the
most similar individual postings. Training uses a stratified holdout set for
validation, then fits the saved model on every valid posting.

From the project root, train it with:

```bash
pip install -r features/resume_analysis/requirements.txt
python -m features.resume_analysis.job_matcher train \
  --data /path/to/all_job_post.csv \
  --model features/resume_analysis/models/job_postings_matcher.joblib
```

Try a saved model without requiring the CSV again:

```bash
python -m features.resume_analysis.job_matcher recommend \
  --text "Python developer with Flask, SQL and AWS experience" \
  --limit 3
```

The model output contains the predicted category plus matching job IDs, titles,
skills and similarity scores. The original `job_matcher.joblib` is retained;
use the new `job_postings_matcher.joblib` artifact with this module. See
`MODEL_TRAINING_GUIDE.md` for dataset preparation, resource estimates,
evaluation advice, and when to consider pretrained embeddings.
