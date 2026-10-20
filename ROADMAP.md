# Roadmap

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

## First evolution proposal: current state

The [five-RFC review](AGENTOPS_RFC_REVIEW.md) and [decisions](AGENTOPS_RFC_DECISIONS.md)
prepare optional documentation, fictional fixtures and selected local acceptance
experiments for step 1. A reference-only resume template and a universal project adoption
guide are prepared. Publication requires exact-tree security review without blocking
findings and exact-commit maintainer authorization; no operational adoption
or measured efficiency improvement is inferred.

Steps 2–4 now have an [experimental acceptance specification](docs/experimental/PERSISTENT_RUNTIME.md)
covering overlapping resources, asynchronous barriers, processes, durable recovery,
idempotency and monotonic accounting. Their implementation and execution remain
PROPOSED. Steps 5–6 remain PROPOSED, with no service or workflow configured here.
