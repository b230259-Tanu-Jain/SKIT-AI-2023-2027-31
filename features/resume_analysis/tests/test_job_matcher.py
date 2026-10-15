from __future__ import annotations

import csv

from features.resume_analysis.job_matcher import load_model, train_model


def test_train_and_recommend(tmp_path):
    dataset = tmp_path / "jobs.csv"
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
    model_path = tmp_path / "matcher.joblib"
    report = train_model(dataset, model_path, test_size=0.5)
    matcher = load_model(model_path)

    assert report["training_rows"] == 4
    assert matcher.predict_category("I build Flask APIs with Python and SQL") == "INFORMATION-TECHNOLOGY"
    assert matcher.recommend_jobs("Python Flask SQL developer", limit=1)[0]["job_title"] == "Python Developer"
