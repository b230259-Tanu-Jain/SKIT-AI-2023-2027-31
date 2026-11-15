# Skill Gap Analysis - Vanshika Choudhary

## Status as of 15 November 2026

An initial command-line flow is implemented for the Form 2 skill-gap sprint
(scheduled 1 November-5 December 2026). It extracts skills from a text-based
PDF resume, selects a role from `data/raw/job_role_skills.csv`, and reports
matched and missing required/preferred skills plus required-skill coverage.
It checks role-specific skill phrases directly against cleaned resume text as
well as using the general resume skill vocabulary.

Run from the repository root with a role name that appears in the dataset:

```bash
python -m features.skill_gap.main path/to/resume.pdf \
  --role "Sr Human Resource Generalist" \
  --data data/raw/job_role_skills.csv
```

Matching currently normalizes case and punctuation, then checks exact skill
names/phrases. A skill reported as missing may be present in the resume under
another phrase. Treat output as a review aid, not as a definitive assessment.
The PDF-to-JSON command and comparisons are covered by the module test suite.
Remaining sprint work includes representative resume review and API/interface
integration.
