# Resume Intelligence - Vanshika Choudhary

## Status as of 6 October 2026

Completed work in this folder:

- Sprint 2: PDF resume text extraction and cleaning with PyPDF.
- Sprint 3 (in progress): NLP-assisted technical skill extraction, plus education and experience extraction.

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
use the new `job_postings_matcher.joblib` artifact with this module.
