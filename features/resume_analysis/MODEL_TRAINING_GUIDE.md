# WorkSphere model training guide

This guide covers the current resume-to-job model and how to build it again. The project does not need to train a large language model from scratch: the existing job model is a small TF-IDF + LinearSVC classifier plus a TF-IDF posting index. It trains on CPU and is appropriate for the dataset currently used by the project.

## 1. Know what is trained

`features/resume_analysis/job_matcher.py` trains two related pieces:

1. A TF-IDF + LinearSVC classifier predicts one broad job category from job-posting text.
2. A TF-IDF cosine-similarity index ranks individual postings against resume text.

These are fitted using job postings, not resume/job suitability labels. Therefore the classifier metrics measure category prediction only. The retrieval scores are text similarity scores, not probabilities that a person will get a job or is qualified for it. The skill-gap feature is a transparent rules-based comparison against the role-skill table, not a learned model.

## 2. Prepare the data

Use a lawful, permitted dataset and retain its source, license, collection date, and preprocessing notes. Do not put private resumes, API keys, or personally identifying data in Git. The training CSV for the matcher must have these columns:

| Column | Meaning |
| --- | --- |
| `job_id` | Stable unique posting identifier |
| `category` | Broad class label used by the classifier |
| `job_title` | Job title |
| `job_description` | Job description text |
| `job_skill_set` | Skills, either as text or a Python-style list string |

The checked-in `data/raw/job_role_skills.csv` is a separate tab-separated role requirements dataset despite its `.csv` extension. It powers skill-gap analysis; it is not the job-postings CSV required by the classifier. Keep a permitted postings file outside version control (for example `data/private/all_job_postings.csv`). Check data quality before training: remove duplicate posting IDs, blank labels, empty text, malformed skill fields, and any personally identifying material. Split by source/company or time where possible to reduce near-duplicate leakage.

## 3. Set up a CPU environment

From the repository root, use Python 3.10–3.12 and a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r features/resume_analysis/requirements.txt
```

The current TF-IDF/SVM pipeline does not use a GPU. For thousands or tens of thousands of short postings, a recent laptop with 8 GB RAM is usually enough; larger data may need more memory. Start with a representative sample before scaling up.

## 4. Train and evaluate

Run from the repository root, changing the input path to your permitted CSV:

```bash
python -m features.resume_analysis.job_matcher train \
  --data data/private/all_job_postings.csv \
  --model features/resume_analysis/models/job_postings_matcher.joblib
```

The command makes a stratified 80/20 holdout split (seed 42), reports accuracy, macro F1, and per-category precision/recall/F1, then fits a final model on all valid rows. It writes the model and a sibling `.metrics.json` report. Keep the validation report with the model version. Macro F1 gives each class equal weight; investigate weak categories and class support instead of relying on accuracy alone. If a category has too few examples for a stratified split, collect more data or combine categories deliberately.

Try a query against the saved model:

```bash
python -m features.resume_analysis.job_matcher recommend \
  --model features/resume_analysis/models/job_postings_matcher.joblib \
  --text "Python developer with SQL, Flask, and AWS experience" \
  --limit 5
```

The checked-in metrics file records a previous run over 1,167 rows with 234 validation rows, 0.9359 accuracy and 0.9368 macro F1. These results are reproducible only when the exact source CSV, preprocessing, dependency versions, and split are available. The source postings CSV is not currently checked into this repository.

## 5. Try the skill-gap feature

This comparison uses the resume parser plus `data/raw/job_role_skills.csv`; it does not require training:

```bash
python -m features.skill_gap.main path/to/resume.pdf \
  --role "Sr Human Resource Generalist" \
  --data data/raw/job_role_skills.csv
```

Use a role name exactly as listed in the dataset. A missing item means the current resume skill vocabulary did not detect it, so review the resume before drawing conclusions. Improve coverage by expanding and reviewing `SKILL_ALIASES` against the permitted role vocabulary.

## 6. When to use a larger model

First establish a labelled evaluation set: human-reviewed resume-to-role relevance judgments, with clear criteria and separate training/validation/test groups. Compare the baseline against pretrained sentence embeddings (for example sentence-transformers) for semantic retrieval. You can index embeddings on CPU; a supported GPU can speed up embedding generation for a large corpus. Fine-tune a pretrained encoder only if you have enough clean labelled pairs, a held-out test set, and compute. Training a transformer from random initialization on this student project dataset is not a sensible first step: it needs far more data and compute and is unlikely to outperform the baseline.

For a larger embedding model, rent a GPU only for the batch embedding or fine-tuning job, save the model/version and evaluation report, and test locally before integrating it. Never upload private resumes or licensed data to a cloud service without permission. Measure ranking quality (such as Recall@K or nDCG@K) on a human-judged test set; classifier F1 does not evaluate recommendation ranking.

## 7. Repeatable handoff checklist

- Record dataset source/license, date, row count, label distribution, and cleaning steps.
- Save the exact training command, Python/dependency versions, random seed, model version, and metrics.
- Keep private input data out of Git; commit code and non-sensitive evaluation summaries only.
- Review errors with a human and make clear that recommendations are decision support, not hiring decisions.
- Retrain only after a data or code change, then compare against the previous held-out results.
