---
name: example-skill
description: Describe what this skill does and the user requests that should activate it.
---

# Skill Title

## Purpose

State the concrete outcome this skill helps the agent deliver.

## When to use

Use this skill when:
- The user asks for [specific task].
- The workflow requires [specific capability].

Do not use it for:
- [Out-of-scope task].

## Inputs

- Required: [input]
- Optional: [input]

Ask only for missing information that materially affects correctness.

## Workflow

1. Inspect the available context and inputs.
2. Confirm constraints and assumptions.
3. Perform the task in explicit, ordered steps.
4. Validate the result against the success criteria.
5. Report the result and any limitations.

## Output

Describe the expected deliverable, format, and required details.

## Decision rules

- If [condition], then [action].
- If [missing or conflicting information], ask the user.
- If [unsafe or destructive action], stop and request approval.

## Quality checks

- [ ] Required content is present.
- [ ] Claims are supported by available evidence.
- [ ] Referenced resources exist.
- [ ] Output meets the user's constraints.

## Examples

### Example request

[Representative user request]

### Expected behavior

[Short description of correct skill behavior]
