"""PDF resume extraction for WorkSphere Sprint 2."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .preprocessing import SECTION_HEADERS, clean_text, contact_details, section_lines, split_lines


class ResumeParser:
    """Extract text from a PDF resume and return a stable starter profile schema."""

    def extract_pdf_text(self, file_path: str | Path) -> str:
        path = Path(file_path)
        if path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF resumes are supported.")
        if not path.is_file():
            raise FileNotFoundError(f"Resume not found: {path}")

        try:
            from pypdf import PdfReader
        except ImportError as error:
            raise RuntimeError(
                "PDF extraction requires pypdf. Install dependencies with "
                "`pip install -r backend/requirement.txt`."
            ) from error

        try:
            reader = PdfReader(str(path))
            pages = [page.extract_text() or "" for page in reader.pages]
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
            # These sections are intentionally text-only until Sprint 3 NLP extraction.
            "education": section_lines(clean_resume_text, SECTION_HEADERS["education"]),
            "experience": section_lines(clean_resume_text, SECTION_HEADERS["experience"]),
            "projects": section_lines(clean_resume_text, SECTION_HEADERS["projects"]),
            "certifications": section_lines(clean_resume_text, SECTION_HEADERS["certifications"]),
            "skills": [],
        }
        return profile

    def parse(self, file_path: str | Path) -> dict[str, Any]:
        return self.build_profile(self.extract_pdf_text(file_path))


def parse_resume(file_path: str | Path) -> dict[str, Any]:
    """Convenience function for API routes and scripts."""
    return ResumeParser().parse(file_path)
