import unittest
from pathlib import Path

from features.resume_analysis.resume_parser import ResumeParser
from features.skill_gap.job_roles import load_job_role_skills


class ResumeProfileTests(unittest.TestCase):
    def test_build_profile_normalises_text_and_sections(self):
        profile = ResumeParser().build_profile(
            "Vanshika Choudhary\n\nvan@example.com  +91 98765 43210\n\n"
            "Education:\nB.Tech CSE\n\nExperience\nDeveloper Intern\n\n"
            "Skills\nPython, SQL"
        )

        self.assertEqual(profile["name"], "Vanshika Choudhary")
        self.assertEqual(profile["email"], "van@example.com")
        self.assertEqual(profile["phone"], "+91 98765 43210")
        self.assertEqual(profile["education"], ["B.Tech CSE"])
        self.assertEqual(profile["experience"], ["Developer Intern"])
        self.assertEqual(profile["skills"], [])

    def test_pdf_extension_is_required(self):
        with self.assertRaises(ValueError):
            ResumeParser().extract_pdf_text("resume.docx")

    def test_job_role_dataset_is_normalised(self):
        dataset_path = Path(__file__).parents[1] / "data/raw/job_role_skills.csv"
        dataset = load_job_role_skills(dataset_path)
        self.assertGreaterEqual(len(dataset), 10)
        self.assertIn("python", dataset.loc[0, "required_skill_list"])


if __name__ == "__main__":
    unittest.main()
