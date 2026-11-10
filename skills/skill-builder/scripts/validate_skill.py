#!/usr/bin/env python3
"""Validate core Agent Skills naming and frontmatter requirements.

This dependency-free checker intentionally validates a conservative subset of
YAML frontmatter. For full YAML/specification validation, also run skills-ref.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")


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
        fields[key] = (value or "").strip().strip("'\"")
    return fields, errors


def validate(skill_file: Path) -> list[str]:
    errors: list[str] = []
    if skill_file.name != "SKILL.md":
        errors.append("The file must be named SKILL.md.")
    if not skill_file.is_file():
        return errors + [f"File does not exist: {skill_file}"]

    fields, parse_errors = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
    errors.extend(parse_errors)

    name = fields.get("name", "")
    description = fields.get("description", "")
    if not name:
        errors.append("Required frontmatter field 'name' is missing or empty.")
    else:
        if len(name) > 64:
            errors.append("'name' must be at most 64 characters.")
        if not NAME_RE.fullmatch(name):
            errors.append("'name' must use lowercase letters, digits, and single hyphens only.")
        if skill_file.parent.name != name:
            errors.append(
                f"Skill directory '{skill_file.parent.name}' must match frontmatter name '{name}'."
            )

    if not description:
        errors.append("Required frontmatter field 'description' is missing or empty.")
    elif len(description) > 1024:
        errors.append("'description' must be at most 1024 characters.")

    body = skill_file.read_text(encoding="utf-8").split("---", 2)
    if len(body) < 3 or not body[2].strip():
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
    print("Note: this lightweight checker is not a full YAML parser or official conformance validator.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
