# Conformance and current evidence

| Scope | Current status | What it does not establish |
| --- | --- | --- |
| Fourteen primary schemas plus common definitions and inactive configuration schema | IMPLEMENTED; local positive/negative fixtures TESTED | Authentication, live authority, deployment, or full operational conformance |
| Structural validation and selected semantic guards | IMPLEMENTED; local tests in reports/local-tests.json | Every possible cross-record relationship or external artifact digest |
| Pure state/deduplication/retry/publication reducers | IMPLEMENTED; synthetic cases TESTED | Durable process scheduling, multiprocess exclusion, network exactly-once effects |
| Synthetic example message reader | IMPLEMENTED; byte preservation and adversarial cases TESTED | Compatibility with external message protocols or historical messages |
| SQLite DDL | IMPLEMENTED; basic in-memory constraints TESTED | Persistent crash recovery, migrations, backups, workers, or transaction implementation |
| Real event adapter, AI executor, publisher and policy issuer | PROPOSED | No remote runtime or two-team execution has been verified here |
| Critical or production operations | Outside the reference profile | No merge, deployment, secret/permission change, or production approval |

A conformant operational profile must demonstrate: authenticated/authorized input,
pinned resource and policy, durable uniqueness and claims, bounded budgets and
retries, cancellation/fencing, evidence integrity, uncertain-effect reconciliation,
independent required review, exact publication readback and authorized closure.

Required fault cases include repeated deliveries/reruns, edited content with the
same ID, concurrent claims, worker crash, late callbacks, ambiguous publication,
missing/corrupt state, permission failure, rate limits, provider disconnection,
new resource revision, revoked grants, prompt injection, own-output loops and ACKs.

Report each claim with implementation version, inputs, revision, environment,
procedure, observable result and limitations. Never promote a result from another
context or a proposed design into a verified AgentOps capability. Human reports,
automated tests, platform observations and documents are different evidence classes.

The reference timestamp/URI checks intentionally enforce a conservative subset.
No general RFC format, security audit, provider compatibility, vulnerability-free
status, or multi-platform certification is implied by passing the current suite.
