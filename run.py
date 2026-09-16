"""Convenient terminal entry point for the currently implemented WorkSphere modules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from features.resume_analysis.resume_parser import parse_resume
from features.skill_gap.job_roles import load_job_role_skills


def main() -> None:
    parser = argparse.ArgumentParser(description="Run available WorkSphere functionality.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-roles", action="store_true", help="Print available role-skill records.")
    group.add_argument("--resume", type=Path, help="Extract a starter profile from a text-based PDF resume.")
    args = parser.parse_args()

    if args.list_roles:
        roles = load_job_role_skills(Path("data/raw/job_role_skills.csv"))
        print(roles[["job_role", "required_skills", "preferred_skills"]].to_string(index=False))
    else:
        print(json.dumps(parse_resume(args.resume), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
