"""Experience extraction helpers for the WorkSphere Resume Intelligence module."""

from __future__ import annotations

import re

from .preprocessing import SECTION_HEADERS, section_lines


ROLE_WORDS = ("intern", "engineer", "developer", "analyst", "designer", "manager", "trainee", "associate")
DATE_RANGE = re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4}\s*(?:-|–|to)\s*(?:present|current|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4})", re.IGNORECASE)


def extract_experience(text: str) -> list[str]:
    """Return relevant experience lines; this does not infer years of experience."""
    entries = section_lines(text, SECTION_HEADERS["experience"])
    if not entries:
        entries = [
            line.strip() for line in text.splitlines()
            if DATE_RANGE.search(line) or any(word in line.lower() for word in ROLE_WORDS)
        ]
    result: list[str] = []
    for entry in entries:
        entry = re.sub(r"\s+", " ", entry).strip()
        if entry and entry not in result:
            result.append(entry)
    return result
