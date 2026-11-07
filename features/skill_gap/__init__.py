"""Job-skill dataset preparation and resume-to-role gap analysis."""

from .job_roles import load_job_role_skills
from .main import analyze_skill_gap

__all__ = ["load_job_role_skills", "analyze_skill_gap"]
