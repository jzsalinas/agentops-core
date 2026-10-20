# Compatibility analysis

Baseline: `f58a5399ccfe75271402f7bc5a55625ecda21baf`. Native AGENTOPS/1 schemas,
their IDs, required properties, enums, closed-object rules and original fixtures are
preserved byte for byte. Native validator/guard/reducer behavior and SQLite DDL are
also preserved. No ProjectConfig mode, enabled execution, dependency or permission
is added. Existing tests must continue to pass without adopting the new artifacts.

| Surface | Proposed use | Compatibility boundary |
| --- | --- | --- |
| ApprovalRequest, Authorization, common.scope | Refer to exact synthetic plan/output digests through existing artifacts/scope | No new action or consent field; trusted issuer and atomic use accounting still external |
| EvidenceBundle, common.artifact | Attach plan, acceptance and projection artifacts by actual digest/length/media type | Existing readers validate the envelope only; optional profile understanding needs negotiation |
| Task.acceptance_criteria | Reference assertion IDs in existing textual criteria | No structured assertion field or automatic acceptance |
| HandoffMessage | Existing evidence_refs and resolution_condition point to current records | Projection is a cache; no permission transfer or new handoff kind |
| Incident, RecoveryAction | Record synthetic privacy/uncertainty category, recovery preconditions and limits | No export of private incidents; compensation remains separately authorized |
| Execution, Assignment, Attempt, Result, Event, metrics | Runtime design references existing contracts | No claim that runtime invariants are implemented; unknown integer-only metrics cannot be emitted as null |
| Policies and coordinator/subagent templates | Optional candidate instructions for adopters | Behavioral changes require explicit version/digest adoption; never auto-reload from main |
| Public allowlist, checksums and reports | Regenerated for this candidate | Passing audit is neither release authorization nor an immutable release identity |

The JSON examples use `profile` values `agentops-effect-plan/0.1-experimental`,
`agentops-evidence-acceptance/0.1-experimental` and
`agentops-destination-projection/0.1-experimental`. These are separately identified
artifact examples, not AGENTOPS/1 record kinds or a new schema catalog. Local
checks exercise selected fixture semantics; they are not a general profile parser.
Unknown/unadopted profiles cannot authorize work or satisfy acceptance by default.

## Future version decision

Recommend a future source MINOR candidate `0.2.0-draft.1`, retaining wire AGENTOPS/1:
this change adds optional profiles and proposed instruction behavior, exceeding a
PATCH as defined by distribution policy. The source metadata remains `0.1.0-draft.1`
until a maintainer explicitly assigns a new version. This branch is unreleased and
must not be distributed as the immutable original candidate, even though that metadata
is intentionally unchanged. Exact source commit and manifests distinguish the bytes.

Adding `effect_plan`/`assertions`/`projection` properties to a closed native record,
new scope actions, or nullable native integer metrics requires a separately versioned
schema catalog and negotiated migration. Strict old readers can reject that data.
If native contracts or authority semantics are broken, use a future wire MAJOR
(AGENTOPS/2) and corresponding source MAJOR under distribution policy. This proposal
does not preapprove such a change. Durable runtime implementation alone does not
require a wire change, and must have its own implementation version and conformance.

Migration for these optional artifacts: owner reviews exact diff and digest, pins the
profile and instructions, validates consumer-specific fixtures, drains/reconciles any
pending work, then records explicit adoption. Rollback removes optional consumption
without restoring old permissions or deleting effect history. Without adoption, keep
existing behavior and reject any requirement depending on an unknown profile.
