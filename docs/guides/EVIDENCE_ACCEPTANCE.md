# Evidence acceptance: optional artifact guide

Candidate artifact profile: `agentops-evidence-acceptance/0.1-experimental`.
Use [assertion examples](../../fixtures/evolution/evidence-acceptance.json)
and [positive/negative cases](../../fixtures/evolution/evidence-cases.json).
The existing EvidenceBundle vocabulary and Task criteria remain authoritative.

Each assertion identifies a claim/criterion, task and subject revision, expected
condition, observed condition, evidence class, producer, procedure/source, artifact
reference/digest, result and limits. Task.acceptance_criteria may name the assertion
ID in existing text. Attach assertions to a bundle; required independent review
checks their coverage and provenance rather than counting PASS labels.

Verify exact artifact bytes/size and subject/revision first. Then verify that the
procedure actually observed the criterion in that environment, and that the evidence
class supports the claim. The synthetic example measures a fictional display layout
from a supplied JSON observation. It is not evidence about an actual device or UI.
Names of artifacts are not observations. Two different names with identical bytes
do not establish two different conditions; equal digests can also be legitimate
deduplication, so reject the unsupported claim rather than banning all equal hashes.

Keep each criterion's outcome separate. Valid coverage remains available when another
criterion fails. A corrected observation produces a new bundle ID with `supersedes_ids`
linking the old bundle, preserving the original and its limits. Reusing a valid result
requires rechecking revision, relevance and provenance; no blanket rerun is required.

A human report remains HUMAN_REPORT. Even when a policy accepts that class for a
particular criterion, it must not be relabeled as PLATFORM_OBSERVATION. A successful
local process cannot establish remote effect, publication approval or deployment.
Record unknown facts as UNKNOWN, and explicitly list unsupported claims. Hashes verify
bytes, not truth, authorship, authorization or independence of observations.

The local fixture predicate compares selected criterion/revision/class/observation
relationships and recomputes observation digests. It cannot authenticate producers,
prove that observations were honestly collected, or replace domain instrumentation
and substantive independent review. Native textual contradiction checks are also
limited; a structurally valid bundle may still be semantically inadequate.
