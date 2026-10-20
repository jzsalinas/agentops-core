# Roadmap

Optional entry path: the [onboarding kit](AGENTOPS_ONBOARDING_ARCHITECTURE.md) is a
local documentation proposal for read-only project assessment and approved
documentary adoption. It neither completes nor depends on the runtime stages below.
Host discovery and consumer installation remain untested and unperformed.

1. Review the draft contracts, privacy boundaries, license, examples, and offline
   validators. Publish source only after explicit maintainer approval.
2. Implement a real single-writer local CLI with SQLite persistence, atomic claims,
   grant consumption, outbox, cancellation, and crash recovery. Test races using
   separate processes; in-memory SQL constraints alone are insufficient.
3. Add a transport adapter that reads an authorized synthetic task and a separate
   executor adapter that starts a bounded real process. Verify input revision and output.
4. Add an isolated publisher and independent reviewer role, with verified correlation,
   evidence, uncertain-effect reconciliation, and a project-specific acceptance policy.
5. Demonstrate optional event-driven operation on a synthetic private test repository
   without a desktop session. Prove persistence across workers and stop conditions.
6. Evaluate other transports/providers and publish conformance profiles only when
   their evidence supports the exact claim. Keep critical operations separately authorized.

All stages after the offline reference implementation are proposed. No date, hosting
service, model, price, or automatic activation is promised. Each stage has a reviewable
artifact and an explicit acceptance decision rather than a claim inherited from use
in another environment.
