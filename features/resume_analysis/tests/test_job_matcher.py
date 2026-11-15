from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from features.resume_analysis.job_matcher import load_model, train_model


class JobMatcherTests(unittest.TestCase):
    def test_train_save_load_predict_and_recommend(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dataset = root / "jobs.csv"
            rows = [
                ("1", "INFORMATION-TECHNOLOGY", "Python Developer", "Build Python APIs using Flask and SQL", "['python', 'flask', 'sql']"),
                ("2", "INFORMATION-TECHNOLOGY", "Data Engineer", "Use Python SQL pipelines and cloud data", "['python', 'sql', 'aws']"),
                ("3", "HR", "HR Manager", "Manage recruitment payroll employee relations", "['recruitment', 'payroll']"),
                ("4", "HR", "Recruiter", "Source candidates and manage employee onboarding", "['recruitment', 'onboarding']"),
            ]
            with dataset.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["job_id", "category", "job_title", "job_description", "job_skill_set"])
                writer.writerows(rows)

            model_path = root / "matcher.joblib"
            report = train_model(dataset, model_path, test_size=0.5)
            matcher = load_model(model_path)

            self.assertEqual(report["training_rows"], 4)
            self.assertEqual(matcher.predict_category("I build Flask APIs with Python and SQL"), "INFORMATION-TECHNOLOGY")
            self.assertEqual(matcher.recommend_jobs("Python Flask SQL developer", limit=1)[0]["job_title"], "Python Developer")

    def test_checked_in_model_artifact_loads_and_returns_matches(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        artifact = repo_root / "features/resume_analysis/models/job_postings_matcher.joblib"
        matcher = load_model(artifact)

        matches = matcher.recommend_jobs("Python SQL data engineering and AWS", limit=3)

        self.assertEqual(len(matches), 3)
        self.assertTrue(matches[0]["job_title"])
        self.assertGreaterEqual(matches[0]["match_score"], 0)


if __name__ == "__main__":
    unittest.main()
