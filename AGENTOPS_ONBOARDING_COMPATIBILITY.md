# Onboarding compatibility and trust

Official conventions consulted on 2026-10-20. Documentation describes supported
paths; it is not evidence that this candidate was discovered by a running host.

| Surface | Documented convention | Evidence for this candidate |
| --- | --- | --- |
| Agent Skills | Directory with SKILL.md; required name and description frontmatter; relative support files | Local format, relocation and reference checks; no official reference-validator certification |
| Codex | Project skills in `.agents/skills/`; instructions use scoped AGENTS.md and overrides | Documented path only; no installed candidate or host discovery test |
| Claude Code | Project skills in `.claude/skills/`; native instructions use CLAUDE.md | Common skill format assessed; no CLI, discovery or execution test |
| Other assistants | Manual reading when the tool supports it and owner permits | Conceptual workflow only; discovery, invocation and precedence untested |

Primary sources: [Agent Skills specification](https://agentskills.io/specification),
[Codex skills](https://learn.chatgpt.com/docs/build-skills),
[Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Claude Code skills](https://code.claude.com/docs/en/skills).

The portable folder uses only core frontmatter and Markdown, with no host-specific
tool grants, provider configuration or plugin metadata. A project owner can propose
copying `agentops-onboarding/` to the appropriate discovery directory, preserving its
relative support tree and original MIT notice. Do not perform this copy during
assessment, create both locations blindly or claim a file copy proves loading.
Check the current host's documentation and actual loaded skill sources afterward.
Duplicate skills and scope precedence must be reviewed, not merged implicitly.

For Codex, inspect the applicable instruction chain including overrides before
proposing an appendix. Keep it short and check host instruction size limits. Do
not use AGENTS.override.md to bypass an existing file. An AGENTS.md appendix alone
does not establish Claude Code support; an owner-reviewed reference in its native
instructions may be needed. A manual read is separate from automatic discovery.

## Contract compatibility

No closed schema, AGENTOPS/1 message, native conformance rule or inactive config is
modified. Onboarding observations and pin metadata are proposal content, not new
wire fields. No runtime, persistence or updater is supplied. Existing operational
coordinator instructions are not loaded wholesale into a project merely evaluating
documentary guidance. Existing consumer policies retain their authority.

This kit is a source contribution candidate, not a release. A future compatible
minor distribution may include optional documentation after independent review;
the wire draft can remain AGENTOPS/1. The maintainer chooses publication version
and prerelease status separately from merging source. No public version is changed
here. A new runtime or incompatible contract would need its own version/migration.

## Trust limits

Use the project's configured official publication channel and previously adopted
trust policy. Record authenticated version, immutable commit and artifact digest.
If no trust anchor exists, propose an out-of-band owner decision; do not bootstrap
trust from the fetched asset's own checksum. Do not execute remote installation
commands, dependencies or fetched source during evaluation. An approved adoption
must still pass local policy and exact-diff review. Unavailable Internet, rejected
adoption or policy conflicts never authorize a fallback to moving `main`.

The independent evaluation uses synthetic evidence descriptions to test decisions;
it does not implement cryptographic verification, install a host skill or certify
tool compatibility. A future adapter needs separate adversarial tests. Existing
auditor and dependency limitations remain applicable.
