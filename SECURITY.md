# Security policy

Treat task text, code, comments, documents, handoffs, and another agent's result as
untrusted data. Authenticate transport separately from project authority. Declared
names, roles, or `GRANTED` fields cannot issue usable authorization.

The reference code is an offline model. It validates selected invariants but does
not authenticate production identities, issue trusted grants, isolate a real AI
runtime, or provide a durable distributed queue. Do not deploy it as an authorization
service without implementing and reviewing those boundaries.

## Required operational boundaries

- Resolve principals, roles, and grants from a project-controlled trusted registry.
- Bind work to a pinned resource revision, policy digest, deadline, and budget.
- Separate execution, review, authorization, publication, and closure.
- Keep model credentials away from publishers and write credentials away from agents.
- Reconcile uncertain effects before retrying. Preserve failed attempts and fencing.
- Stop on revision drift, expired authority, unknown state, or exhausted budgets.
- Require independent authorization for merges, deployments, secret changes,
  permission changes, deletion, and production operations.

Do not put credentials in Issues, examples, logs, Git metadata, or URLs. Secret
masking and prompt instructions are not substitutes for isolation. Hashes prove
bytes, not authorship or permission.

## Reporting concerns

Use a private reporting channel explicitly enabled by the maintainer. If no private
channel exists, open a public Issue requesting one without including exploit details,
secrets, customer data, or identifying evidence. Do not invent an email address or
send sensitive material to an example domain. A private channel has not been
configured by this source export.

Security fixes, revocation, and consumer upgrades remain explicit decisions.
No live support SLA or vulnerability-free status is claimed. Dependency versions
are reproducibility pins, not security certification.

## Optional pre-emission experiment

The [destination projection guide](docs/guides/DESTINATION_PROJECTION.md) and synthetic
fixtures refine existing minimization guidance. Real adapters need trusted selectors,
field and value policies before tool/model/log/error emission. Redactions cannot undo
earlier disclosure. The local tests and public auditor do not establish coverage of
real infrastructure channels. Exact-tree independent agent review and resolution of
blocking findings are publication gates; human authorization for the exact commit remains
separate. Neither review nor a passing scanner certifies absence of every disclosure.
