"""Train and use a transparent content-based resume-to-job matching model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


REQUIRED_COLUMNS = {"job_id", "category", "job_title", "job_description", "job_skill_set"}


def _clean_text(value: object) -> str:
    text = str(value or "").lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _posting_text(row: pd.Series) -> str:
    """Prioritise title and stated skills, then retain supporting description text."""
    title = _clean_text(row["job_title"])
    skills = _clean_text(row["job_skill_set"])
    description = _clean_text(row["job_description"])
    return " ".join((title, title, title, skills, skills, description))


@dataclass
class JobMatcher:
    """A fitted TF-IDF job index used to rank relevant jobs for a resume profile."""

    vectorizer: TfidfVectorizer
    job_matrix: Any
    jobs: pd.DataFrame

    def match(self, resume_text: str, top_k: int = 5) -> list[dict[str, Any]]:
        if not resume_text or not resume_text.strip():
            raise ValueError("Resume text is required for job matching.")
        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        resume_vector = self.vectorizer.transform([_clean_text(resume_text)])
        scores = cosine_similarity(resume_vector, self.job_matrix).ravel()
        limit = min(top_k, len(scores))
        indices = scores.argsort()[::-1][:limit]
        return [
            {
                "job_id": str(self.jobs.iloc[index]["job_id"]),
                "category": self.jobs.iloc[index]["category"],
                "job_title": self.jobs.iloc[index]["job_title"],
                "job_skill_set": self.jobs.iloc[index]["job_skill_set"],
                "match_score": round(float(scores[index]) * 100, 2),
            }
            for index in indices
        ]


def train_job_matcher(dataset_path: str | Path) -> JobMatcher:
    """Train a TF-IDF retrieval model from the supplied job-posting CSV.

    The source has no labelled resume/job match pairs, so this intentionally
    trains a content-based retrieval model instead of an unsupported classifier.
    """
    dataset_path = Path(dataset_path)
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Job-posting dataset not found: {dataset_path}")

    jobs = pd.read_csv(dataset_path)
    jobs.columns = jobs.columns.str.strip().str.lower()
    missing = REQUIRED_COLUMNS - set(jobs.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    jobs = jobs.dropna(subset=["job_title", "job_description", "job_skill_set"]).copy()
    for column in REQUIRED_COLUMNS:
        jobs[column] = jobs[column].fillna("").astype(str).str.strip()
    jobs = jobs[(jobs["job_title"] != "") & (jobs["job_description"] != "")].copy()
    if len(jobs) < 2:
        raise ValueError("At least two complete job postings are required for training.")

    documents = jobs.apply(_posting_text, axis=1).tolist()
    vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.98,
        max_features=50000,
        sublinear_tf=True,
        strip_accents="unicode",
    )
    job_matrix = vectorizer.fit_transform(documents)
    model_jobs = jobs[["job_id", "category", "job_title", "job_skill_set"]].reset_index(drop=True)
    return JobMatcher(vectorizer=vectorizer, job_matrix=job_matrix, jobs=model_jobs)


def save_job_matcher(matcher: JobMatcher, model_path: str | Path) -> Path:
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(matcher, model_path, compress=3)
    return model_path


def load_job_matcher(model_path: str | Path) -> JobMatcher:
    model_path = Path(model_path)
    if not model_path.is_file():
        raise FileNotFoundError(f"Trained model not found: {model_path}")
    matcher = joblib.load(model_path)
    if not isinstance(matcher, JobMatcher):
        raise ValueError("The selected file is not a WorkSphere job-matching model.")
    return matcher
