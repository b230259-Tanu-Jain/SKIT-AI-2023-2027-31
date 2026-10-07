"""Education extraction helpers for the WorkSphere Resume Intelligence module."""

from __future__ import annotations

import re

from .preprocessing import SECTION_HEADERS, section_lines


EDUCATION_TERMS = (
    "b.tech", "btech", "b.e", "bachelor", "b.sc", "bsc", "m.tech", "mtech",
    "m.e", "master", "m.sc", "msc", "diploma", "class xii", "class x", "cgpa",
    "university", "college", "school",
)


def extract_education(text: str) -> list[str]:
    """Return education entries from an education section or degree-containing lines."""
    entries = section_lines(text, SECTION_HEADERS["education"])
    if not entries:
        entries = [
            line.strip() for line in text.splitlines()
            if any(term in line.lower() for term in EDUCATION_TERMS)
        ]
    result: list[str] = []
    for entry in entries:
        entry = re.sub(r"\s+", " ", entry).strip()
        if entry and entry not in result:
            result.append(entry)
    return result
