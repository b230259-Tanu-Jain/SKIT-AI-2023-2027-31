"""Skill extraction for the WorkSphere Resume Intelligence module.

The extractor uses spaCy tokenisation when available and matches against a
transparent technical-skill vocabulary.  Keeping the vocabulary local makes
the detected skills easy to explain and expand during project evaluation.
"""

from __future__ import annotations

import re


SKILL_ALIASES = {
    "python": ("python",),
    "java": ("java",),
    "c++": ("c++", "cpp"),
    "c": (" c ", "c language"),
    "javascript": ("javascript", "java script"),
    "typescript": ("typescript",),
    "sql": ("sql", "mysql", "postgresql", "sqlite"),
    "html": ("html", "html5"),
    "css": ("css", "css3"),
    "react": ("react", "react.js", "reactjs"),
    "node.js": ("node.js", "nodejs", "node js"),
    "express.js": ("express", "express.js", "expressjs"),
    "mongodb": ("mongodb", "mongo db"),
    "pandas": ("pandas",),
    "numpy": ("numpy",),
    "scikit-learn": ("scikit-learn", "scikit learn", "sklearn"),
    "machine learning": ("machine learning", "ml"),
    "deep learning": ("deep learning",),
    "nlp": ("natural language processing", "nlp"),
    "spacy": ("spacy", "spaCy"),
    "tensorflow": ("tensorflow",),
    "pytorch": ("pytorch", "py torch"),
    "fastapi": ("fastapi",),
    "django": ("django",),
    "flask": ("flask",),
    "git": ("git", "github"),
    "docker": ("docker",),
    "aws": ("aws", "amazon web services"),
    "linux": ("linux",),
    "power bi": ("power bi", "powerbi"),
    "tableau": ("tableau",),
    "excel": ("excel", "ms excel", "microsoft excel"),
    "figma": ("figma",),
    "rest api": ("rest api", "restful api", "restful services"),
    "data structures": ("data structures",),
    "algorithms": ("algorithms",),
}


def _normalise(text: str) -> str:
    original_text = text
    try:
        import spacy

        document = spacy.blank("en")(text)
        tokenised_text = " ".join(token.text for token in document)
        # Preserve the original text too: tokenisation intentionally separates
        # punctuation in names such as ``scikit-learn`` and ``node.js``.
        text = f"{original_text} {tokenised_text}"
    except ImportError:
        # The module stays usable in a minimal environment, but requirements.txt
        # records spaCy as the expected Sprint 3 dependency.
        pass
    return f" {re.sub(r'\s+', ' ', text.lower())} "


def extract_skills(text: str) -> list[str]:
    """Return unique recognised technical skills in predictable display order."""
    searchable_text = _normalise(text)
    found: list[str] = []
    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = rf"(?<![a-z0-9+#.]){re.escape(alias.lower())}(?![a-z0-9+#.])"
            if re.search(pattern, searchable_text):
                found.append(skill)
                break
    return found
