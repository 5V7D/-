#!/usr/bin/env python3
"""Run a lightweight Agent Skills structure/frontmatter check.

This dependency-free checker validates a deliberately limited subset of YAML.
It is not a replacement for the official `skills-ref validate` command.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")


def valid_skill_name(name: str) -> bool:
    """Mirror skills-ref name validation, including NFKC normalization."""
    normalized = unicodedata.normalize("NFKC", name.strip())
    if (
        not normalized
        or len(normalized) > 64
        or normalized != normalized.lower()
        or normalized.startswith("-")
        or normalized.endswith("-")
        or "--" in normalized
    ):
        return False
    return all(char.isalnum() or char == "-" for char in normalized)


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["SKILL.md must begin with YAML frontmatter opening '---'."]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, ["YAML frontmatter closing '---' was not found."]

    fields: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = KEY_RE.match(line)
        if not match:
            errors.append(f"Unsupported or malformed frontmatter line {number}: {line}")
            continue
        key, value = match.groups()
        if key in fields:
            errors.append(f"Duplicate frontmatter field '{key}' on line {number}.")
        fields[key] = (value or "").strip().strip("'\\\"")
    return fields, errors


def validate(skill_file: Path) -> list[str]:
    errors: list[str] = []
    if skill_file.name != "SKILL.md":
        errors.append("The file must be named SKILL.md.")
    if not skill_file.is_file():
        return errors + [f"File does not exist: {skill_file}"]

    content = skill_file.read_text(encoding="utf-8")
    fields, parse_errors = parse_frontmatter(content)
    errors.extend(parse_errors)
    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append("Required frontmatter field 'name' is missing or empty.")
    else:
        if not valid_skill_name(name):
            errors.append("'name' must be 1-64 lowercase Unicode alphanumeric characters and single hyphens (after NFKC normalization).")
        directory_name = unicodedata.normalize("NFKC", skill_file.parent.name)
        normalized_name = unicodedata.normalize("NFKC", name.strip())
        if directory_name != normalized_name:
            errors.append(f"Skill directory '{skill_file.parent.name}' must match frontmatter name '{name}' after NFKC normalization.")

    if not description:
        errors.append("Required frontmatter field 'description' is missing or empty.")
    elif len(description) > 1024:
        errors.append("'description' must be at most 1024 characters.")

    parts = content.split("---", 2)
    if len(parts) < 3 or not parts[2].strip():
        errors.append("Markdown instruction body after frontmatter must not be empty.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", type=Path, help="Path to a skill directory or its SKILL.md")
    args = parser.parse_args()
    skill_file = args.skill / "SKILL.md" if args.skill.is_dir() else args.skill
    errors = validate(skill_file)
    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"VALIDATION PASSED: {skill_file}")
    print("Limited local check only; run skills-ref validate for full specification validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
