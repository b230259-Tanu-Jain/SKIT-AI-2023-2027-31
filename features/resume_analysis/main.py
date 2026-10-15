"""Command-line entry point for the completed Resume Intelligence scope."""

from __future__ import annotations

import argparse
import json

from .resume_parser import parse_resume


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract skills, education and experience from a text-based PDF resume."
    )
    parser.add_argument("resume", help="Path to a text-based PDF resume")
    args = parser.parse_args()
    print(json.dumps(parse_resume(args.resume), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
