"""Compare extracted resume skills with a selected role's skill requirements.

This first version is deliberately interpretable: it reports exact normalized
skill matches against the supplied role dataset. It does not claim that a
similarity score is a probability or infer skills that are absent from a CV.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Iterable

from features.resume_analysis.resume_parser import parse_resume
from features.skill_gap.job_roles import load_job_role_skills


def normalize_skill(skill: str) -> str:
    """Normalize case and punctuation so common spelling variants compare."""
    value = skill.casefold().strip()
    value = value.replace("&", " and ").replace("c++", "cplusplus")
    value = value.replace("c#", "csharp").replace(".net", " dotnet ")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def _unique_skills(skills: Iterable[str]) -> list[str]:
    unique: dict[str, str] = {}
    for skill in skills:
        original = str(skill).strip()
        normalized = normalize_skill(original)
        if normalized:
            unique.setdefault(normalized, original)
    return list(unique.values())


def analyze_skill_gap(resume_skills: Iterable[str], required_skills: Iterable[str], preferred_skills: Iterable[str] = ()) -> dict:
    """Return matched and missing required/preferred skills and coverage."""
    resume = _unique_skills(resume_skills)
    required = _unique_skills(required_skills)
    preferred = _unique_skills(preferred_skills)
    resume_index = {normalize_skill(skill) for skill in resume}

    def compare(targets: list[str]) -> tuple[list[str], list[str]]:
        matched = [skill for skill in targets if normalize_skill(skill) in resume_index]
        missing = [skill for skill in targets if normalize_skill(skill) not in resume_index]
        return matched, missing

    matched_required, missing_required = compare(required)
    matched_preferred, missing_preferred = compare(preferred)
    return {
        "resume_skills": resume,
        "required_skills": {
            "matched": matched_required,
            "missing": missing_required,
            "coverage_percent": round(100 * len(matched_required) / len(required), 1) if required else 0.0,
        },
        "preferred_skills": {"matched": matched_preferred, "missing": missing_preferred},
        "matching_method": "normalized exact skill-name matching",
        "note": "A missing skill means it was not detected in the resume text; it may still be present but phrased differently.",
    }


def _find_role(roles, requested_role: str):
    target = requested_role.casefold().strip()
    exact = roles[roles["job_role"].str.casefold() == target]
    if exact.empty:
        choices = roles["job_role"].tolist()
        suggestions = [role for role in choices if target in role.casefold()]
        if not suggestions:
            suggestions = choices[:10]
        raise ValueError(f"Role '{requested_role}' not found. Example available roles: {', '.join(suggestions)}")
    return exact.iloc[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare a PDF resume with a role in the WorkSphere skill dataset.")
    parser.add_argument("resume", help="Path to a text-based PDF resume")
    parser.add_argument("--role", required=True, help="Exact job_role value from the role dataset")
    parser.add_argument("--data", default="data/raw/job_role_skills.csv", help="Role-skill dataset path")
    args = parser.parse_args()

    try:
        roles = load_job_role_skills(args.data)
        role = _find_role(roles, args.role)
        profile = parse_resume(args.resume)
        result = {
            "job_role": role["job_role"],
            "analysis": analyze_skill_gap(
                profile["skills"], role["required_skill_list"], role["preferred_skill_list"]
            ),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
