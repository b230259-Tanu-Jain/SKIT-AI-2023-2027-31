"""PDF resume extraction for WorkSphere Sprint 2."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .education_extractor import extract_education
from .experience_extractor import extract_experience
from .preprocessing import SECTION_HEADERS, clean_text, contact_details, section_lines, split_lines
from .skill_extractor import extract_skills


class ResumeParser:
    """Extract text from a PDF resume and return a stable starter profile schema."""

    def extract_pdf_text(self, file_path: str | Path) -> str:
        path = Path(file_path)
        if path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF resumes are supported.")
        if not path.is_file():
            raise FileNotFoundError(f"Resume not found: {path}")

        # PyMuPDF is the primary extractor selected for the project.  pypdf is
        # retained as a lightweight fallback so the feature remains usable if
        # only the original Sprint 2 dependency is installed.
        try:
            import fitz

            with fitz.open(path) as document:
                pages = [page.get_text("text") for page in document]
        except ImportError:
            try:
                from pypdf import PdfReader
            except ImportError as error:
                raise RuntimeError(
                    "PDF extraction requires PyMuPDF or pypdf. Install dependencies with "
                    "`pip install -r features/resume_analysis/requirements.txt`."
                ) from error
            try:
                reader = PdfReader(str(path))
                pages = [page.extract_text() or "" for page in reader.pages]
            except Exception as error:
                raise ValueError(f"Could not read the PDF resume: {path.name}") from error
        except Exception as error:
            raise ValueError(f"Could not read the PDF resume: {path.name}") from error

        text = clean_text("\n".join(pages))
        if not text:
            raise ValueError("No selectable text was found. Use a text-based PDF or add OCR first.")
        return text

    def build_profile(self, raw_text: str) -> dict[str, Any]:
        clean_resume_text = clean_text(raw_text)
        lines = split_lines(clean_resume_text)
        name = lines[0] if lines and "@" not in lines[0] and len(lines[0]) <= 80 else None
        contact = contact_details(clean_resume_text)
        profile: dict[str, Any] = {
            "name": name,
            **contact,
            "raw_text": raw_text,
            "clean_text": clean_resume_text,
            # Sprint 3: return usable extracted entities, not just raw sections.
            "education": extract_education(clean_resume_text),
            "experience": extract_experience(clean_resume_text),
            "projects": section_lines(clean_resume_text, SECTION_HEADERS["projects"]),
            "certifications": section_lines(clean_resume_text, SECTION_HEADERS["certifications"]),
            "skills": extract_skills(clean_resume_text),
        }
        return profile

    def parse(self, file_path: str | Path) -> dict[str, Any]:
        return self.build_profile(self.extract_pdf_text(file_path))


def parse_resume(file_path: str | Path) -> dict[str, Any]:
    """Convenience function for API routes and scripts."""
    return ResumeParser().parse(file_path)
