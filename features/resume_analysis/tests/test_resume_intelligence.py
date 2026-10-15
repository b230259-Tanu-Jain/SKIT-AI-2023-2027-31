"""Standard-library tests for the Resume Intelligence scope through 15 October."""

from __future__ import annotations

import unittest

from features.resume_analysis import ResumeParser, extract_skills
from features.skill_gap.job_roles import load_job_role_skills


SAMPLE_RESUME = """Aarav Sharma
aarav@example.com | +91 98765 43210

TECHNICAL SKILLS
Python, SQL, Pandas, scikit-learn, FastAPI, Docker and AWS

EDUCATION
B.Tech in Computer Science, Example University, 2026

EXPERIENCE
Data Analyst Intern | Jan 2025 - Present
Built Python data pipelines and SQL dashboards.

PROJECTS
Resume intelligence application using Python and FastAPI.
"""


class ResumeIntelligenceTests(unittest.TestCase):
    def test_profile_contains_all_sprint_three_extractions(self) -> None:
        profile = ResumeParser().build_profile(SAMPLE_RESUME)

        self.assertEqual(profile["name"], "Aarav Sharma")
        self.assertEqual(profile["email"], "aarav@example.com")
        self.assertEqual(profile["phone"], "+91 98765 43210")
        self.assertEqual(
            profile["skills"],
            ["python", "sql", "pandas", "scikit-learn", "fastapi", "docker", "aws"],
        )
        self.assertEqual(profile["education"], ["B.Tech in Computer Science, Example University, 2026"])
        self.assertIn("Data Analyst Intern | Jan 2025 - Present", profile["experience"])

    def test_skill_extraction_avoids_partial_word_matches(self) -> None:
        self.assertEqual(extract_skills("The candidate enjoys javascript and C++ but not javabeans."), ["c++", "javascript"])

    def test_tab_separated_role_dataset_is_prepared(self) -> None:
        dataset_path = "data/raw/job_role_skills.csv"
        roles = load_job_role_skills(dataset_path)

        self.assertGreater(len(roles), 0)
        self.assertIn("required_skill_list", roles.columns)
        self.assertTrue(all(isinstance(skills, list) for skills in roles["required_skill_list"]))


if __name__ == "__main__":
    unittest.main()
