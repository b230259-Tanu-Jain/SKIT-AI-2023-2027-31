"""Train and use the WorkSphere resume-to-job matching model.

The model has two complementary parts trained from job postings:

* a TF-IDF + linear SVM classifier that identifies the most relevant job
  category for resume text; and
* cosine-similarity retrieval that returns the individual postings most
  similar to the resume.

Keeping the estimator and the postings together in one joblib payload means
the application does not need the source CSV at prediction time.
"""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any, Iterable

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


REQUIRED_COLUMNS = {"job_id", "category", "job_title", "job_description", "job_skill_set"}
MODEL_VERSION = "1.0"


def _as_text(value: object) -> str:
    """Convert CSV values into clean text without leaking ``nan`` tokens."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    return " ".join(str(value).split())


def _skills_as_text(value: object) -> str:
    """Turn the dataset's Python-list skill field into searchable text."""
    text = _as_text(value)
    if not text:
        return ""
    try:
        parsed = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return text
    if isinstance(parsed, (list, tuple, set)):
        return " ".join(_as_text(item) for item in parsed)
    return text


def _posting_text(row: pd.Series) -> str:
    """Give the short title a little extra weight while retaining full context."""
    title = _as_text(row["job_title"])
    return " ".join((title, title, _as_text(row["job_description"]), _skills_as_text(row["job_skill_set"])))


def load_postings(csv_path: str | Path) -> pd.DataFrame:
    """Load, validate, clean and de-duplicate the supplied job-postings CSV."""
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"Job-postings dataset not found: {path}")
    postings = pd.read_csv(path, encoding="utf-8-sig")
    postings.columns = postings.columns.str.strip().str.lower()
    missing = REQUIRED_COLUMNS - set(postings.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    postings = postings[list(REQUIRED_COLUMNS)].copy()
    for column in REQUIRED_COLUMNS:
        postings[column] = postings[column].map(_as_text)
    postings = postings[(postings["category"] != "") & ((postings["job_title"] != "") | (postings["job_description"] != ""))]
    postings["text"] = postings.apply(_posting_text, axis=1)
    postings = postings[postings["text"] != ""].drop_duplicates(subset=["job_id"]).reset_index(drop=True)
    if postings["category"].nunique() < 2:
        raise ValueError("At least two job categories are required to train the model.")
    return postings


def _make_pipeline() -> Pipeline:
    return Pipeline(
        [
            # ``min_df=1`` also keeps the trainer useful for a small, local
            # project dataset; the production CSV still has enough rows for
            # robust validation.
            ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
            ("classifier", LinearSVC(C=1.0, class_weight="balanced")),
        ]
    )


def train_model(csv_path: str | Path, model_path: str | Path, test_size: float = 0.2) -> dict[str, Any]:
    """Train, evaluate, and save a model payload; return its validation report."""
    postings = load_postings(csv_path)
    texts = postings["text"]
    labels = postings["category"]
    x_train, x_test, y_train, y_test = train_test_split(
        texts, labels, test_size=test_size, random_state=42, stratify=labels
    )
    validation_model = _make_pipeline()
    validation_model.fit(x_train, y_train)
    predictions = validation_model.predict(x_test)

    full_model = _make_pipeline()
    full_model.fit(texts, labels)
    vectorizer = full_model.named_steps["tfidf"]
    job_matrix = vectorizer.transform(texts)
    display_columns = ["job_id", "category", "job_title", "job_description", "job_skill_set"]
    payload = {
        "model_version": MODEL_VERSION,
        "pipeline": full_model,
        "job_matrix": job_matrix,
        "postings": postings[display_columns].to_dict(orient="records"),
        "metadata": {
            "training_rows": int(len(postings)),
            "categories": sorted(postings["category"].unique().tolist()),
            "random_state": 42,
            "test_size": test_size,
        },
    }
    destination = Path(model_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, destination)

    report = {
        "model_path": str(destination),
        "training_rows": int(len(postings)),
        "validation_rows": int(len(y_test)),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "macro_f1": round(float(f1_score(y_test, predictions, average="macro")), 4),
        "classification_report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
    }
    metrics_path = destination.with_suffix(".metrics.json")
    metrics_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["metrics_path"] = str(metrics_path)
    return report


class JobMatcher:
    """Runtime interface for a saved WorkSphere job-matching model."""

    def __init__(self, payload: dict[str, Any]):
        self.pipeline: Pipeline = payload["pipeline"]
        self.job_matrix = payload["job_matrix"]
        self.postings: list[dict[str, str]] = payload["postings"]
        self.metadata: dict[str, Any] = payload.get("metadata", {})

    def predict_category(self, resume_text: str) -> str:
        text = _as_text(resume_text)
        if not text:
            raise ValueError("Resume text cannot be empty.")
        return str(self.pipeline.predict([text])[0])

    def recommend_jobs(self, resume_text: str, limit: int = 5) -> list[dict[str, Any]]:
        """Return the most textually similar postings with a readable score."""
        text = _as_text(resume_text)
        if not text:
            raise ValueError("Resume text cannot be empty.")
        if limit < 1:
            raise ValueError("limit must be at least 1.")
        vectorizer = self.pipeline.named_steps["tfidf"]
        scores = cosine_similarity(vectorizer.transform([text]), self.job_matrix).ravel()
        indices = np.argsort(scores)[::-1][:limit]
        results: list[dict[str, Any]] = []
        for index in indices:
            posting = self.postings[int(index)]
            results.append(
                {
                    "job_id": posting["job_id"],
                    "category": posting["category"],
                    "job_title": posting["job_title"],
                    "job_skill_set": posting["job_skill_set"],
                    "match_score": round(float(scores[index]) * 100, 2),
                }
            )
        return results


def load_model(model_path: str | Path) -> JobMatcher:
    """Load a model created by :func:`train_model`."""
    path = Path(model_path)
    if not path.is_file():
        raise FileNotFoundError(f"Model not found: {path}")
    payload = joblib.load(path)
    required = {"pipeline", "job_matrix", "postings"}
    if not isinstance(payload, dict) or not required.issubset(payload):
        raise ValueError("This is not a compatible WorkSphere job-matcher model.")
    return JobMatcher(payload)


def _main() -> None:
    parser = argparse.ArgumentParser(description="Train or query the WorkSphere job matcher.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    train_parser = subparsers.add_parser("train", help="train and save a model")
    train_parser.add_argument("--data", required=True, help="path to all_job_post.csv")
    train_parser.add_argument("--model", default="features/resume_analysis/models/job_postings_matcher.joblib")
    query_parser = subparsers.add_parser("recommend", help="find jobs for resume text")
    query_parser.add_argument("--model", default="features/resume_analysis/models/job_postings_matcher.joblib")
    query_parser.add_argument("--text", required=True, help="resume text or extracted resume content")
    query_parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    if args.command == "train":
        print(json.dumps(train_model(args.data, args.model), indent=2))
    else:
        matcher = load_model(args.model)
        print(json.dumps({"predicted_category": matcher.predict_category(args.text), "matches": matcher.recommend_jobs(args.text, args.limit)}, indent=2))


if __name__ == "__main__":
    _main()
