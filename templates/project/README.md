# Project adoption template

This template is inactive: DRAFT, execution disabled, MANUAL_ONESHOT, no repositories,
no credentials, no provider and no enabled executor. Its schema prevents activation.
Do not turn a valid configuration into an authorization claim.

In a separately approved operational implementation, project owners establish stable
identities for `team-a`, `team-b`, and roles such as `agent-reviewer`; bind trusted
principals; choose resources, revision, executor and transport; define authority,
review, budgets, retention and cancellation; pin versions/digests; record adoption.

Use the coordinator, subagent and autonomy instructions as reviewed templates, never
as live prompts loaded from a mutable public branch. Configuration evolution and
new triggers require their own schema, tests and migration review. Keep credentials
in an approved external store; contracts contain references, not values.

The optional evolution additions in coordinator/subagent instructions and [RESUME](RESUME.md)
are local contribution candidates. Manual documentary use can organize references and
review without claiming durable or operational conformance. Owners must explicitly adopt
their exact version/digest; no ProjectConfig change or runtime activation is included.
