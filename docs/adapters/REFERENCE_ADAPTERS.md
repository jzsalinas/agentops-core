# Reference adapter designs

These are proposed integration interfaces. No provider SDK, workflow, runner,
credential, scheduler, or service is installed by this distribution. The core
contracts remain independent of GitHub, Codex, and any specific hosting provider.

| Trigger mode | Proposed invocation | Availability boundary |
| --- | --- | --- |
| MANUAL_ONESHOT | Operator invokes one bounded reconciliation pass | Requires an available host and authorized bindings |
| ON_EVENT_ACTIONS | An approved GitHub Actions workflow handles an admitted event | Requires explicitly configured workflow, provider access and durable state |
| SCHEDULED_POLL | An approved scheduler queries overlapping pages/cursors | Scheduler tick is not task authorization or guaranteed delivery |
| WEBHOOK_WORKER | A persistent receiver verifies and durably records a delivery before worker execution | Requires an operated service, verification, storage and recovery |
| LOCAL_STARTUP | An approved environment startup hook performs reconciliation | Does not receive events while the host is off or wake a desktop remotely |

All modes call the same ingest/reconcile ports, apply the same authority policy,
and preserve business identities across deliveries and reruns. Never run independent
ledger copies for the same scope. Changing mode requires a controlled transfer of
ownership, pending effects, fencing and budget state.

## Optional GitHub design

Read an allowlisted synthetic request, verify actual actor and resource revision,
record it durably, and invoke an explicitly configured executor. Isolate publishers
from untrusted repository content and model credentials. Read back each effect by
ID, target and digest. A label or comment selects data; it never grants permission.

For a two-role automatic trial, one reviewed controller may sequence analysis,
publication, a second role's new execution, and a correlated response. This avoids
assuming every automated comment triggers another workflow. Jobs must preserve
state and evidence across hosts. This design has not been run by the reference model.

## Optional Codex design

A configured adapter can invoke a noninteractive CLI, action wrapper, or SDK and
translate observed events/results into AgentOps contracts. Pin its version, model,
prompt, capabilities and policy. Establish its own supported authentication and
cost limits. Do not copy a user's desktop credentials or assume subscription/API
entitlements are interchangeable. No particular implementation is required by the standard.

## Synthetic message adapter

`agentops_reference/example_handoff.py` reads only the documented synthetic
EXAMPLE-HANDOFF/1 fixture dialect. It returns an additive normalized view and unchanged
source bytes, always with scheduling/authority disabled. It rejects ambiguous or
unsafe YAML. Unknown forms require review; this is not proof of interoperability
with another project's existing protocol.

## Candidate profile integration boundaries

Optional [effect plans](../guides/EFFECT_PLAN.md),
[criterion observations](../guides/EVIDENCE_ACCEPTANCE.md) and
[destination projections](../guides/DESTINATION_PROJECTION.md) require explicit adopted
profile bindings. Trusted adapters must supply actual authority, revision, provenance,
settlement and destination-policy facts. The local predicates simulate those inputs;
they do not implement these adapter ports. The
[persistent experiment](../experimental/PERSISTENT_RUNTIME.md) defines future evidence gates.
