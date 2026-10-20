# Effect plan and consent: optional artifact guide

Candidate artifact profile: `agentops-effect-plan/0.1-experimental`. This guide
refines existing authority and reliability rules. It grants no permissions.
See the [plan example](../../fixtures/evolution/effect-plan.json) and
[decision fixtures](../../fixtures/evolution/effect-cases.json).

Prepare the objective, task/revision, pinned resource, policy digest, exact output
digest, destination, business marker and expected effect before asking for any
missing decision. Attach the plan as an `EvidenceBundle.artifacts` entry and bind
its digest and the exact output digest to `ApprovalRequest.scope.artifact_digests`.
A trusted issuer may then issue Authorization under its adopted policy; an approved
request or plan is not itself a consumable grant. Preparation, review request and
actual distribution are distinct effects even if the interface calls all of them Save.

For each mutating step record its action, target, preconditions, before-state,
completion signal, postcondition, timeout behavior and allowed recovery. The example
permits only `publish_result` for one fictional report. Deployment and other critical
operations remain outside this profile. A real adapter must bind the target and
business marker to trusted resource/policy/output records; native scope has no new
destination field. It must compare the actual payload digest, count aggregate effects,
and reserve grants/budgets atomically; `guard_execution` alone does not do all of this.

Immediately before an effect reload authenticated authority and the current resource,
policy, task, assignment/lease/fence and output. Any material drift stops affected
work and requires a new reviewed baseline. Do not rely on copied plan values as facts.
Complete one action and observe settlement before another action on the same resource.
Record the observation in an attempt/result; an exclusive operator can still race
its own asynchronous request.

| Observation | Required boundary |
| --- | --- |
| Same effect, routine confirmation | Continue only if current grant, tool policy and human instruction all permit it |
| Human instruction says consult every new dialogue | Obtain the required decision even for a routine confirmation |
| New destination, agreement, permission or distribution | Stop that step and prepare a new concrete decision request |
| Pending asynchronous action | Wait/read/reconcile within the authorized budget; do not click the next mutation |
| Timeout with uncertain effect | Record UNKNOWN and reconcile by original marker/target/digest; never blind resend |
| Matching effect already confirmed | Preserve evidence and return without another send |

A readback mismatch is an incident, not success. Missing/inconclusive readback does
not prove absence. Reconciliation and compensation can require their own scoped
authority. The stricter applicable rule always prevails; silence and elapsed time
cannot expand a grant. Unknown dialogue classification stops for review.

The local decision table takes simulated trusted facts as inputs. It tests a proposed
decision boundary and the existing publication reducer; it does not authenticate a
human, classify a real dialogue, execute a tool or establish durable enforcement.
