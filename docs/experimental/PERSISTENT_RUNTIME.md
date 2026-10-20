# First persistent runtime experiment

Status: PROPOSED. This specifies a future experiment; no runtime is implemented or
tested here. It refines roadmap steps 2–4, with event-driven/provider operation in
later stages. A CLI interface, DDL or synthetic prototype does not prove an operational
runtime. No service deployment, scheduler or hosted workflow is authorized by this design.

## Implementation boundary

Use an on-disk transactional store, one controller writer and at least two independent
claimant processes. A separate bounded real executor process and an isolated publisher
must preserve identities and grants across restarts. A separately durable synthetic
receiver records effects by stable marker and exact target/body digest. It must support
fault injection and lookup/readback; its results establish only that isolated experiment.

Implement authenticated admission/policy ports, task/resource revision checks,
atomic overlapping-resource claims, compare-and-swap record revisions, leases and
monotonic fencing, grant/budget reservation with attempts, cancellation and exact
outbox intents. The current DDL alone omits parts of this transaction model; review
migrations and resource-lock/budget storage before using it. Serialize asynchronous
actions within each resource as well as across workers.

Commit admission before ACK. Commit reservation/attempt/outbox intent before dispatch.
Commit readback before accepting/closing. Never hold a local transaction as a claim of
remote atomicity. Reserve or conservatively consume uncertain uses/effects according
to an explicit policy; never refund them merely because a process crashed. Recovery
must preserve monotonic consumed counts and reconcile the original marker before retry.
Reject same-key edited payloads, and prevent a lease timeout from bypassing reconciliation.

## Required fault matrix and oracles

| Case | Injection | Observable acceptance oracle |
| --- | --- | --- |
| C1 overlapping claims | Barrier releases two OS processes for same resource, including different tasks | Exactly one current owner; losing process cannot start an effect; one committed reservation |
| C2 crash before commit | Kill writer inside reservation transaction | Rollback leaves no partial claim/use/attempt/outbox; restart can safely decide from durable state |
| C3 crash after intent, before send | Kill after durable outbox commit | Restart sees original marker and reserved use; at most one eventual receiver effect |
| C4 crash after remote effect | Receiver commits, publisher dies before local confirmation | Restart looks up same target/marker/digest; records CONFIRMED with no second effect/use |
| C5 ambiguous absence | Receiver hides readback after timeout | UNKNOWN remains blocked; no blind retry or refund |
| C6 stale worker | Lease expires/reclaim after reconciliation; deliver old callback | Fence increases; old callback preserved as late evidence and cannot integrate/publish |
| C7 replay/conflict | Repeated deliveries, alternate trigger/rerun/host; same business key; then edited payload | Same task/effect identity; no extra consumption; edited same-ID content quarantined |
| C8 revocation/cancel/drift | Change grant/policy/task/resource after prepare, before effect; cancellation races callback | Affected new effect blocked; pending effects reconciled; old evidence cannot close new revision |
| C9 budget race | Parent/children compete for last attempt/use/effect/cost reservation | Aggregate cap never exceeded; counters survive restart and no-progress limit stops loops |
| C10 state integrity | Missing/corrupt store, interrupted migration, stale backup restore | Fail closed; reviewed recovery/migration; no rollback of grants, fences or publication history |
| C11 readback conflict | Marker found with different body or destination | Quarantine; no acceptance, closure or second send |
| C12 inner async race | One operator starts delayed mutation then requests another | Second mutation waits for settlement; UNKNOWN goes to reconciliation |
| C13 isolation | Untrusted input asks for grant/credential; executor attempts publisher access | No issuer or publisher privilege acquired; deny before effect and before private output |
| C14 metrics | Provider omits usage; clock/source observation unavailable | Tokens/cost stay null; unknown required integer metrics block native result emission; no invented zero |

Run each race with synchronized barriers, both controlled schedules and repeated
stress runs. Record repeat count, seed/schedule, process roles, fault point, store
state before/after restart, receiver readbacks, immutable IDs/digests, grant/budget/fence
history and assertions. A test runner must fail on any invariant violation, missing
required observation or unexpected process survival; successful exit alone is insufficient.

## Evidence required to leave PROPOSED

Retain implementation commit/digest, storage/schema and migration versions, OS/runtime,
durability settings, command/procedure, number of independent processes, injected
faults, results including failures, and limitations in an authorized evidence bundle.
Prove cold restart using the same durable store and a separately retained receiver
store, rather than reinitializing a clean database. Include backup/restore and
integrity tests; a JSON result file without reproducible observations is insufficient.

Independent technical/security review and maintainer acceptance are separate gates.
Success may be reported as TESTED for this isolated persistent experiment only. Real
provider integration, authenticated production authority, unattended hosting, external
protocol compatibility and production reliability still require their own evidence.
No exactly-once network guarantee, host-independent availability or measured efficiency
benefit follows. Report physical attempts, tool calls and business effects separately;
unknown cost/token metrics remain null, and no ROI is inferred from document counts.
