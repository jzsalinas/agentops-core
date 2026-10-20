# Local PR proposal — not submitted

Proposed title: Add optional effect, evidence and destination profiles without changing AGENTOPS/1

Base: updated `main`, verified at `f58a5399ccfe75271402f7bc5a55625ecda21baf`.
Local branch: `evolution/rfc-first-review`. No remote PR or branch has been created.
The candidate uses the existing approved public commit identity. No release version
has been assigned. Publication requires maintainer authorization for the exact local
commit; opening a PR does not authorize merging or activating consumers.

## Proposed description

An exact grant, a PASS result and a filename allowlist do not by themselves prove
that an asynchronous effect is settled, an acceptance condition was observed or an
inventory is safe for its destination. This change prepares optional guides and
fictional examples that make those boundaries explicit while preserving AGENTOPS/1.

It includes an assessment and partial dispositions for all five RFC, native artifact
references with actual digests, positive/negative local experiments, candidate
coordinator/subagent instructions and a minimal reference-only resume template.
It also refines the proposed persistent-runtime milestone with concurrency, recovery
and idempotency acceptance oracles; no runtime is implemented or claimed operational.

The [five-RFC decisions](../AGENTOPS_RFC_DECISIONS.md) accept RFC-01/02/05 only as
optional guidance and bounded experiments, limit RFC-03 to a derived reference
projection, and retain RFC-04 as a proposed persistent-runtime experiment. The
[project adoption guide](PROJECT_ADOPTION.md) describes a voluntary consumer update
PR, compatibility review, tests, owner approval and recorded activation. It installs
no integration and updates no consumer automatically.

Validation: the original 49 tests pass, plus 26 new offline tests (75 total). The new
table includes 19 effect-boundary cases; criterion tests reject false coverage and
preserve partial results; projector tests capture synthetic output/log/error channels.
The public payload passes the existing auditor with a private denylist and exact
allowlist/checksums. See [test results](../AGENTOPS_TEST_RESULTS.md) for scope and limits.

Compatibility: native schemas, original fixtures, guards/reducers, DDL and dependency
pins are unchanged. Optional artifacts require explicit adoption. A future source
MINOR candidate `0.2.0-draft.1` is recommended; no version is incremented in this PR
proposal. New native fields/actions or nullable integer metrics require a versioned
catalog/migration, and incompatible semantics require a future wire MAJOR.

Publication gates: separate security-agent review of the exact candidate tree, resolution
of blocking findings and maintainer authorization for the exact commit. The independent
review identified and prompted correction of Git-metadata link counting and overbroad
link-rejection wording/coverage; 75 test methods remain, with expanded negative subcases.
Exact-tree review evidence is retained separately; task separation is not institutional
or human certification. Future version assignment and consumer adoption remain separate
decisions. Synthetic checks do not verify live
authority, real pre-emission channels, observation provenance, persistent recovery or
efficiency benefits. Existing MIT and third-party notices remain intact.
