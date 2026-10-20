# Minimal resume projection (optional candidate template)

Mode: MANUAL_DOCUMENTARY unless a separately adopted durable runtime is available.
This is a regenerable cache of references, never a ledger or a permission source.
Keep stable instructions separate from this small current-state index and from
immutable historical records. Do not copy credentials or ephemeral session handles.

| Item | Reference to reload from authoritative records |
| --- | --- |
| Snapshot | Read time, projection digest, authoritative store/reference and integrity status |
| Adoption | Standard/profile version, instruction digest, policy digest and explicit adoption record |
| Work | Task ID/task_revision/record_revision/resource revision, acceptance criteria; Execution and TaskAssignment IDs/digests |
| Ownership | Current agent/executor, exclusive resources, lease/fencing and cancellation state from assignment/execution |
| Evidence | Latest EvidenceBundle/ExecutionResult IDs/digests, class, observation time, supported/unsupported criteria and limits |
| Effect | Last confirmed effect reference/readback or UNKNOWN; original outbox marker/digest through trusted store |
| Authority | Authorization IDs/record revisions/digests to reload; current, consumed, expired and revoked states distinguished |
| Recovery | Incident/RecoveryAction references and preconditions; unresolved references stay UNKNOWN |
| Limits | Attempt/parent budget references, known metrics and explicit unknowns; no reset on resume |
| Next step | Proposed action, supporting references, required decision, stop conditions and expected observation |

Fill only references and bounded summaries; blank/unknown authority never means allowed.
If a required digest/reference cannot be verified, stop affected execution. Refresh
grants, issuer bindings, revocation, policy, task/resource revision, fence, budget and
remote effect immediately before any action. Reacquire tool bindings through the
authorized adapter; a previous tool handle is not a durable resource identity.

If the last effect is UNKNOWN, reconcile the original effect before any resend.
A consumed grant remains consumed after a restart. Changed resource or policy
requires rebaseline and new acceptance as applicable. Missing/corrupt projection
does not justify reconstructing authority from conversation memory.

For manual documentary use explicitly record: no durable ledger/atomic reservations
demonstrated; external effects blocked until authority and remote state are reconciled
through an authorized mechanism. This mode does not claim operational conformance.
HandoffMessage.evidence_refs and resolution_condition can refer to the same current
records; do not add new fields to the closed HandoffMessage or ProjectConfig schemas.
