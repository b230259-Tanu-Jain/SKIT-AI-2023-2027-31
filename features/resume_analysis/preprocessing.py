"""Small, dependency-free helpers for preparing extracted resume text."""

from __future__ import annotations

import re
import unicodedata
from typing import Iterable


SECTION_HEADERS = {
    "education": ("education", "academic background", "qualifications"),
    "experience": ("experience", "work experience", "employment history", "internships"),
    "skills": ("skills", "technical skills", "core competencies", "technologies"),
    "projects": ("projects", "academic projects", "personal projects"),
    "certifications": ("certifications", "certificates", "licenses"),
}


def clean_text(text: str) -> str:
    """Normalise common PDF extraction artefacts while retaining paragraph breaks."""
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("\x00", "").replace("\u00ad", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_lines(text: str) -> list[str]:
    return [line.strip(" \t•-–") for line in text.splitlines() if line.strip()]


def _normalise_heading(value: str) -> str:
    return re.sub(r"[^a-z ]", "", value.lower()).strip()


def section_lines(text: str, headers: Iterable[str]) -> list[str]:
    """Return lines after a recognised heading, stopping at the next heading."""
    lines = split_lines(text)
    heading_set = {header.lower() for header in headers}
    all_headings = {heading for values in SECTION_HEADERS.values() for heading in values}
    start = next(
        (index + 1 for index, line in enumerate(lines) if _normalise_heading(line.rstrip(":")) in heading_set),
        None,
    )
    if start is None:
        return []

    result: list[str] = []
    for line in lines[start:]:
        if _normalise_heading(line.rstrip(":")) in all_headings:
            break
        result.append(line)
    return result


def contact_details(text: str) -> dict[str, str | None]:
    """Extract basic contact details without making claims about skills or experience."""
    email = re.search(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", text, re.IGNORECASE)
    phone = re.search(r"(?<!\w)(?:\+?\d[\d .()\-]{8,}\d)(?!\w)", text)
    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
    }
