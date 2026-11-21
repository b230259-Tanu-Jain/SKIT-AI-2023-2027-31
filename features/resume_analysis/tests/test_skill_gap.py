from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

from features.skill_gap.main import analyze_skill_gap
from features.skill_gap.job_roles import load_job_role_skills


REPO_ROOT = Path(__file__).resolve().parents[3]


class SkillGapTests(unittest.TestCase):
    def test_skill_gap_normalizes_case_and_punctuation(self) -> None:
        result = analyze_skill_gap(
            ["Power BI", "C++", "Python"],
            ["power bi", "C++", "SQL"],
            ["Python", "Docker"],
        )

        self.assertEqual(result["required_skills"]["matched"], ["power bi", "C++"])
        self.assertEqual(result["required_skills"]["missing"], ["SQL"])
        self.assertEqual(result["required_skills"]["coverage_percent"], 66.7)
        self.assertEqual(result["preferred_skills"]["matched"], ["Python"])

    def test_pdf_to_skill_gap_cli_outputs_json_without_runtime_warning(self) -> None:
        roles = load_job_role_skills(REPO_ROOT / "data/raw/job_role_skills.csv")
        role = roles.iloc[0]
        skill = role["required_skill_list"][0]

        with tempfile.TemporaryDirectory() as directory:
            resume_path = Path(directory) / "resume.pdf"
            document = pymupdf.open()
            page = document.new_page()
            page.insert_text((72, 72), f"Sample Candidate\nTECHNICAL SKILLS\n{skill}")
            document.save(resume_path)
            document.close()

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "features.skill_gap.main",
                    str(resume_path),
                    "--role",
                    str(role["job_role"]),
                    "--data",
                    "data/raw/job_role_skills.csv",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            recommendations = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "features.resume_analysis.job_matcher",
                    "recommend-resume",
                    "--resume",
                    str(resume_path),
                    "--limit",
                    "2",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertNotIn("RuntimeWarning", completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["job_role"], role["job_role"])
        self.assertIn(skill, result["analysis"]["required_skills"]["matched"])
        self.assertEqual(recommendations.returncode, 0, recommendations.stderr)
        recommendation_result = json.loads(recommendations.stdout)
        self.assertEqual(len(recommendation_result["matches"]), 2)
        self.assertTrue(recommendation_result["matches"][0]["job_title"])


if __name__ == "__main__":
    unittest.main()
