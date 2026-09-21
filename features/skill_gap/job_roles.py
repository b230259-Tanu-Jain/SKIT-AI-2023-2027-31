"""Job-role skill dataset preparation completed in Sprint 1."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"job_role", "required_skills", "preferred_skills"}


def _split_skills(value: object) -> list[str]:
    return [skill.strip().lower() for skill in str(value).split("|") if skill.strip()]


def load_job_role_skills(file_path: str | Path) -> pd.DataFrame:
    """Load and validate the role-skill reference data for future comparisons."""
    dataset = pd.read_csv(file_path)
    dataset.columns = dataset.columns.str.strip().str.lower()
    missing = REQUIRED_COLUMNS - set(dataset.columns)
    if missing:
        raise ValueError(f"Missing required dataset columns: {sorted(missing)}")

    dataset["job_role"] = dataset["job_role"].fillna("").astype(str).str.strip()
    dataset = dataset[dataset["job_role"] != ""].copy()
    dataset["required_skill_list"] = dataset["required_skills"].apply(_split_skills)
    dataset["preferred_skill_list"] = dataset["preferred_skills"].apply(_split_skills)
    return dataset.reset_index(drop=True)
