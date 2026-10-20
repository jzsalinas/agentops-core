# AGENTOPS/1 — draft specification

AgentOps defines portable contracts for coordinating, executing, communicating,
supervising, and verifying autonomous AI agent teams. A protocol is not an execution
platform, a permission grant, a provider API, or proof that an agent has run.

## Evidence vocabulary

IMPLEMENTED means an artifact exists for the stated scope. TESTED means a named
check executed with an observable result. VERIFIED means evidence supports a specific
claim within its stated inputs, revision, environment, and limitations. PROPOSED
means design without sufficient implementation evidence. BLOCKED means a required
condition or authority is missing. None is a workflow state. Local synthetic tests
do not verify remote activation, human acceptance, or production behavior.

## Contracts

All fourteen primary contracts carry `schema_version=AGENTOPS/1`, a typed `kind`,
stable `id`, project scope, timestamp, and record revision. See the machine-readable
files in `schemas/1/` for every required property and enum.

| Contract | Responsibility |
| --- | --- |
| AgentIdentity | Durable logical agent, team, responsible owner, role, optional runtime binding, registry digest |
| TeamIdentity | Stable team, responsible owners and member agents, registry revision |
| Task | Objective, typed action, executing target, independent review target, resource revision, acceptance criteria, budget, policy, and states |
| TaskAssignment | Claimed task/revision, agent/executor/execution, exclusive resources, lease, fencing, authorization reference |
| Event | Immutable fact, source/target, correlation and immediate cause, payload digest/ref, delivery provenance |
| HandoffMessage | Business communication, task/revision, parties, evidence, requested action, exit condition, optional preserved source snapshot |
| Execution | Assignment and task linkage, executor, optional parent, authorization/policy, attempts, budget, cancellation |
| ExecutionAttempt | One physical attempt, ordinal, fence, start/end, outcome/failure, evidence and metrics |
| Authorization | Trusted issuer decision, grantee, exact task/resource/action/digests, validity window, use limit and consumption |
| ApprovalRequest | Prepared bundle and concrete scope, eligible decision makers, reason, expiry and decision reference |
| EvidenceBundle | Evidence class, environment/procedure, pinned subject, artifacts/digests, supported and unsupported claims, limitations |
| ExecutionResult | Attempt/revision outcome, evidence, limitations, confirmed effects, metrics, human actions still needed |
| Incident | Categorized failure or uncertainty, affected attempt, evidence, known/unknown effects and recovery references |
| RecoveryAction | Reconcile/retry/cancel/rebaseline/escalate/compensate with preconditions, limits and independent authority where needed |

The additional ProjectConfig schema describes an inactive template, not a runtime
activation contract. It intentionally rejects enabled execution and operational
credentials. Adding new modes requires separately reviewed configuration design.

## Identity, scope, and authority

A principal identifies an authenticated subject at an issuer. An owner is a
responsible authority in a project-controlled registry. An agent is a logical role;
an executor is a runtime instance. Display names, model names, account access,
and fields in received messages cannot authenticate or authorize any of them.

IDs use `urn:agentops:<namespace>:<kind>:<opaque>`. Assign once; do not derive them
from a session ordinal, PID, model, or visible username. Delivery, event, task,
execution, attempt, evidence, and effect identities are distinct. Example namespaces
and domains in this distribution are reserved/synthetic and resolve only locally.

`task_revision` changes for material scope/resource changes. `record_revision`
changes for mutable snapshots using compare-and-swap. Event, HandoffMessage,
EvidenceBundle, and ExecutionResult are immutable records with revision 1. Preserve
past records and link successors rather than rewriting evidence.

`correlation_id` identifies the stable Task; `causation_id` identifies the immediate
Event. Cross-task work preserves the causal Event chain and each task's own scope.
Subtasks link parent executions and consume parent budgets. Unresolved source
references remain explicitly unresolved; do not fabricate a causal link.

Resource revision UNKNOWN permits recording an incomplete request. It prevents
execution, verified acceptance, or closure for that revision. Any new SHA invalidates
applicable evidence/acceptance until revalidated under the project policy.

## Independent state dimensions

| Dimension | States |
| --- | --- |
| Receipt | RECORDED, ACKNOWLEDGED, QUARANTINED, REJECTED |
| Execution | NOT_SCHEDULED, QUEUED, CLAIMED, RUNNING, SUCCEEDED, FAILED, BLOCKED, CANCELLED, STALE, EXPIRED |
| Review | NOT_REQUESTED, PENDING, CHANGES_REQUESTED, ACCEPTED, REJECTED, STALE |
| Authorization | NOT_EVALUATED, PENDING, GRANTED, DENIED, EXPIRED, REVOKED, CONSUMED |
| Publication | NOT_REQUESTED, PENDING, SENDING, CONFIRMED, UNKNOWN, FAILED |
| Closure | OPEN, CLOSED, SUPERSEDED |

Persist before transport acknowledgement. A business ACK changes receipt only;
it is not execution, approval, or acceptance. A successful process is not an
accepted result. Publication requires matching remote ID, target and body readback.
UNKNOWN effects require reconciliation. CLOSED requires a current successful result,
required acceptance, confirmed publication, and valid evidence; it does not close
a repository issue, merge code, deploy, or express a human's personal vote.

An approved ApprovalRequest does not issue its own Authorization. A trusted policy
adapter verifies the decision and creates a consumable grant. Verify issuer,
grantee, scope, revision, policy, time, revocation and remaining uses at the boundary
of each effect. Reserve uses atomically with attempts. Silence does not approve;
credential possession does not authorize. Grants for analysis, publication, critical
operations, and human decisions are distinct.

## Reliability and budgets

Define a business execution key as SHA-256 of a UTF-8 compact JSON array of strings:
`[project_id,task_id,task_revision_decimal,recipient_role_id,action,resource_revision]`.
No whitespace, Unicode normalization, floating point, or ambiguous delimiters.
The task fixes repository/resource scope; do not move it between repositories.

Persist independent uniqueness for transport deliveries, business events, execution
keys, and effect keys. Same identity with different content is a conflict requiring
quarantine, not a new implicit request. Cross-mode delivery preserves business identity.
A lease needs an owner, expiry and monotonic fencing. A late callback cannot integrate
under an expired or superseded fence. Reclaim only after checking the previous worker
and reconciling effects. A local transaction cannot make a remote API effect atomic.

An outbox records exact target, body digest, stable marker and authorization before
sending. On timeout, locate/read back the original effect before retrying; inconclusive
absence remains blocked. Do not claim universal exactly-once network delivery.

Budgets aggregate parent and child usage: attempts, wall time, model tokens, cost,
external effects, hops and no-progress exchanges. Unknown metrics are null, not zero.
Every policy specifies numeric limits. The reference example uses at most two
execution attempts, three calls for a transient read, no blind write retry, four
substantive hops and two no-progress exchanges before one authorized escalation.
These are profile choices, not entitlements granted by this specification.

## Evidence and review

Evidence classes are AUTOMATED_LOCAL, INSTRUMENTED, PLATFORM_OBSERVATION,
HUMAN_REPORT and DOCUMENTARY. Artifacts identify exact bytes by digest, size, media
type and authorized reference. `claims_not_supported` must be nonempty. A hash
proves bytes, not authorship, permission, deployment, or actual behavior.

Verify bundle digests, resource revision, producer, access, methods, coverage,
limitations and acceptance requirements. Never download arbitrary artifact URLs
from message text. A source-preserving adapter retains original bytes and source
metadata without interpreting declared identities as grants. The synthetic example
profile in this repository demonstrates that boundary, not external compatibility.

## Validation and evolution

Strict native schemas reject unknown fields and versions. The offline registry
resolves all references locally. The reference validator explicitly checks an ASCII
absolute-URI subset and RFC3339-shaped, calendar-valid timestamps with explicit
zone; it rejects leap seconds and unsupported forms. This conservative profile is
not a complete internationalized-URI or general format validator.

Structural validation does not authenticate a sender or resolve every external
reference. Semantic guards cover selected relationships, not all operational
requirements. See conformance and release gates for the limits of tested claims.
Any change to accepted messages, policy decisions, instructions, or runtime behavior
requires compatibility analysis and explicit consumer adoption.

## Optional evolution artifacts under review

The proposed [effect plan](../../guides/EFFECT_PLAN.md),
[criterion acceptance](../../guides/EVIDENCE_ACCEPTANCE.md) and
[destination projection](../../guides/DESTINATION_PROJECTION.md) guides compose the
existing contracts through digest-bearing artifacts. They do not extend native schemas,
grant authority or establish operational conformance. The
[compatibility report](../../../AGENTOPS_COMPATIBILITY_REPORT.md) specifies separate
profile adoption and future version boundaries. Native validation remains unchanged.
