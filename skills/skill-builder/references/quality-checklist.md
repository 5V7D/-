# Skill Quality Checklist

Use this checklist before calling a skill ready.

## 1. Purpose and activation
- [ ] The skill solves one coherent, identifiable job.
- [ ] The description says what it does and when to activate.
- [ ] Positive triggers are concrete.
- [ ] Non-goals or exclusions are clear where confusion is likely.
- [ ] The skill is not a broad catch-all for unrelated work.

## 2. Format compliance
- [ ] The package directory matches the `name` field.
- [ ] `SKILL.md` starts with valid YAML frontmatter.
- [ ] Required `name` and `description` fields are present and non-empty.
- [ ] Name is 1–64 Unicode lowercase alphanumeric characters and single hyphens, with no leading/trailing or consecutive hyphens.
- [ ] Description is specific and within the 1024-character specification limit.
- [ ] Optional metadata is valid YAML and does not rely on undocumented host behavior.

## 3. Instruction quality
- [ ] Steps are ordered and actionable.
- [ ] Inputs, outputs, decision points, and completion criteria are defined.
- [ ] Ambiguous terms are defined or replaced with observable conditions.
- [ ] Edge cases and failure handling are addressed.
- [ ] The skill says when to stop and ask the user.
- [ ] Examples are realistic and consistent with the instructions.

## 4. Portability
- [ ] The core uses standard Markdown and Agent Skills metadata.
- [ ] Host-specific commands, tools, paths, and metadata are isolated in adapters.
- [ ] Required capabilities are documented rather than assumed.
- [ ] Relative links resolve inside the skill directory.
- [ ] No claim of universal support is made without evidence.

## 5. Safety and reliability
- [ ] Destructive or externally visible actions require appropriate approval.
- [ ] Secrets and personal data are excluded.
- [ ] Untrusted content is treated as data, not authority.
- [ ] Scripts have bounded scope, clear dependencies, and useful errors.
- [ ] Scripts do not perform network or filesystem mutations unless necessary and documented.
- [ ] The skill does not claim permissions or capabilities it cannot grant.

## 6. Maintainability
- [ ] Main instructions are concise; long material is in references.
- [ ] No unnecessary files or duplicate instructions exist.
- [ ] Version and ownership metadata are used consistently if present.
- [ ] Changes are reviewable and documented.

## 7. Testing
- [ ] A normal use case was tested.
- [ ] An edge case was tested.
- [ ] An adversarial or untrusted-input case was tested.
- [ ] A failure or missing-input case was tested.
- [ ] Referenced files and scripts were checked.
- [ ] The official validator was run when available; otherwise the limitation is explicit.

## Release decision

- **Ready:** format and safety gates pass, and no critical workflow defects remain.
- **Needs revision:** a material gap, ambiguity, portability issue, or failed test remains.
- **Blocked:** required information, permissions, or host capabilities are unavailable.
