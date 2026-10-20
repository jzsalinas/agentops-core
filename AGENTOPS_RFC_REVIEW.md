# First evolution: independent technical RFC review

Status: local contribution candidate; public push requires exact-commit maintainer
authorization after independent security review. Baseline: `f58a5399ccfe75271402f7bc5a55625ecda21baf` (AGENTOPS/1,
source candidate `0.1.0-draft.1`). Read-only remote verification found the same
`main` tip before creating the evolution branch. Review date: 2026-10-19.

This review assesses five generalized proposals against the published repository.
Historical practices are neither AgentOps adoption nor runtime conformance evidence.
No causal productivity, cost, reliability or agent-count benefit has been measured.
Only fictional examples and newly executed local checks support this proposal.

## Comparison against existing artifacts

| RFC | Already covered | Residual problem | Technical disposition |
| --- | --- | --- | --- |
| 01 Effect Plan and Consent | Specification authority/reliability; `Authorization.scope`, `ApprovalRequest`; autonomy policy; `guard_execution`; `publication_outcome`; coordinator/subagent templates | Preparation versus distribution, dialogue classification and completion barriers within one operator need concrete examples | Accept optional guide/artifact and offline decision fixtures; defer live enforcement |
| 02 Evidence Acceptance Profile | `Task.acceptance_criteria`; `EvidenceBundle` classes, claims, artifacts, limitations and supersession; selected `validate_semantics` checks; conformance review | A PASS or byte digest can be irrelevant to the actual criterion; textual claim disjointness is insufficient | Accept criterion-to-observation guide and synthetic acceptance checks; domain validation stays outside Core |
| 03 Resume Projection | Task/Execution/Assignment/Authorization/Evidence/Incident/Recovery/Handoff contracts; version pinning and explicit adoption in distribution guide | Reconstructing current state from history can lose consumed grants or UNKNOWN effects | Accept minimal derived template; reject another ledger, authority source or activation mode |
| 04 Runtime Milestone | Roadmap steps 2–5; architecture ports; adapter designs; SQLite DDL; pure reducers and in-memory tests | Durable transactions, cross-process races and recovery remain unverified | Refine experimental milestone and fault matrix only; runtime implementation and results deferred |
| 05 Destination Evidence Projection | Security policy; adapter context minimization; `EvidenceBundle.redactions`; Incident/RecoveryAction; public auditor, file allowlist and checksums | Filtering after emission cannot undo disclosure; filenames do not constrain inventory contents | Accept destination guide and synthetic pre-emission projector tests; defer integration with real tool boundaries |

## Incompatibilities and overreach avoided

All native schemas are closed. Do not add `effect_plan`, `assertions`, `checkpoint`,
`destination_policy` or new metrics inside existing records. Use referenced artifact
bytes with independent experimental profile identifiers. Existing readers still
validate only the native artifact envelope; they do not thereby understand a profile.

`common.scope.actions` supports only `analyze_read_only`, `publish_result` and
`review_result`. This proposal cannot authorize arbitrary UI transactions, deployment,
deletion or permission changes. Examples restrict effects to a synthetic report.
The plan refines an already granted effect; it never interprets vague consent as a grant.

`guard_execution` checks selected trusted-record relationships. It does not authenticate
an issuer, reserve uses atomically, compare every artifact digest, count aggregate
effects or prove a remote destination. The profile experiment adds illustrative checks,
without silently claiming those capabilities for the guard or changing its behavior.

RFC-04 overgeneralizes nullable metrics: `common.metrics.tokens` and `cost_minor` allow
null, while `wall_seconds` and `external_effects` require integers. Unknown values for
the latter must block emission of a completed native metrics record, or remain in a
separate diagnostic artifact until known. Zero must not stand for unknown. Making
those native fields nullable would change accepted data and needs a versioned catalog.

The existing ledger DDL is incomplete as an implementation: business claims alone
do not enforce exclusion of overlapping resources across different tasks; no complete
budget transaction, worker, migration or recovery system exists. New tables alone
would not demonstrate these properties. A single writer still needs resource locking
and barriers for asynchronous actions inside one operator.

Requiring an exact dialogue script, one domain's commands, mandatory multiagent
delegation, automatic consumer upgrades, a universal evidence oracle, or an additional
runtime contract catalog would add fragility without evidence of benefit.

## Evidence and independence limits

This is an independent assessment of proposal content against the baseline, not an
independent human security approval. A separate security-agent review is recorded
outside the public payload against exact candidate trees. Task separation does not
establish institutional independence. Public emission requires resolving all blocking
findings and maintainer authorization for the exact commit. The bounded public audit
supplements content review and is not a
forensic absence-of-disclosure guarantee. Private operational material is excluded.

See [decisions](AGENTOPS_RFC_DECISIONS.md), [compatibility](AGENTOPS_COMPATIBILITY_REPORT.md),
[plan](AGENTOPS_EVOLUTION_PLAN.md) and [executed checks](AGENTOPS_TEST_RESULTS.md).
