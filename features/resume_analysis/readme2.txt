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

The output is a JSON profile with raw/clean text, contact details, recognised skills, education, experience, projects, and certifications.

Not yet started (scheduled later): semantic career-role matching, skill-gap comparison, readiness scoring, and full-system integration.
