# Skill Gap Analysis - Vanshika Choudhary

## Status as of 11 November 2026

An initial command-line flow is implemented for the Form 2 skill-gap sprint
(scheduled 1 November-5 December 2026). It extracts skills from a text-based
PDF resume, selects a role from `data/raw/job_role_skills.csv`, and reports
matched and missing required/preferred skills plus required-skill coverage.

Run from the repository root with a role name that appears in the dataset:

```bash
python -m features.skill_gap.main path/to/resume.pdf \
  --role "Sr Human Resource Generalist" \
  --data data/raw/job_role_skills.csv
```

Matching currently normalizes case and punctuation, then checks exact skill
names. A skill reported as missing may be present in the resume under another
phrase or may not be in the resume extractor's vocabulary. Treat output as a
review aid, not as a definitive assessment. Next work in this sprint is to
expand and review skill aliases, validate results on representative resumes,
and integrate the output with the API and interface.
