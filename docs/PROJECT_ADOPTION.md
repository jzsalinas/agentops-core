# Voluntary project adoption of a new AgentOps version

This is a universal documentary workflow. It installs no integration and changes no
consumer project. Publishing a standard commit, branch, PR or release never updates
consumers automatically. A PR is a proposal, not a published release or an adoption.
Each project's authorized owner controls its own activation, resources and permissions.

Keep source/package version, wire protocol, schema catalog, optional artifact profiles,
instructions, runtime, adapter bindings and consumer policy separately pinned. A source
version does not imply runtime availability. This evolution retains AGENTOPS/1 and
proposes optional artifacts; its recommended future version is not an existing release.

## Seven reviewable steps

1. **Detect a published version.** Inspect only the project's configured trusted
   publication channel. Record the announced version, immutable source commit, package
   digest and release notes, and verify their provenance using the project's adopted
   trust policy. An unmerged branch, mutable `main` reference or notification alone is
   insufficient. With no published version, stop at an evaluation proposal; do not
   invent a release or treat a proposed version string as one. Detection can be manual.

2. **Compare with the project pin.** Read the current adoption record and inventory
   every adopted component/digest. Fetch candidate material into an isolated review
   area without executing it. Compare source, schema IDs/enums/required fields,
   validators, instructions, profiles, dependency pins and license notices. Review
   the entire skipped range if several versions were missed. If the pin or content
   cannot be resolved and verified, stop the affected update; do not infer it from
   conversation memory or choose the newest version automatically.

3. **Evaluate compatibility.** Apply the standard's compatibility report and the
   consumer's own fixtures and policy. Strict readers can reject additive fields.
   Distinguish optional profile negotiation from native contract changes, and changes
   in instructions from purely editorial updates. Identify migrations, state/backup
   requirements, dependency and adapter assumptions, permission differences and
   unsupported claims. A new standard cannot enlarge a consumer's grant, budget or
   capability. Record a go/no-go decision and unresolved issues before proposing activation.

4. **Prepare a consumer update PR.** An authorized contributor may prepare a PR in
   that consumer's repository, with only the reviewed pins, instructions, optional
   profiles, fixtures and migration documents. Include current/proposed versions and
   digests, the exact diff, compatibility findings, expected behavior, tests and their
   limits, rollback procedure and activation plan. Opening this PR needs authority in
   that project; this guide itself grants none. Do not bundle credentials, automatic
   dependency upgrades or service/workflow installation. Adoption can remain documentary.

5. **Run local acceptance tests.** Validate native schemas and the consumer's actual
   pinned-profile fixtures in an authorized isolated environment. Exercise applicable
   negative cases: stale revision, consumed/revoked grants, UNKNOWN effects, evidence
   coverage, destination privacy and unsupported profiles. For an operational update,
   require that implementation's migration/restart/concurrency tests as applicable;
   AgentOps's offline suite cannot substitute for them. Retain inputs, implementation
   version, procedure, results, environment and limits. Unknown measurements stay unknown.

6. **Obtain owner approval.** The project's authorized responsible owner reviews the
   exact consumer PR commit/digests, tests, migration, backup/recovery and activation
   scope. Standard maintainers, peers, CI success and release notifications do not
   issue that approval. Requested independent review or additional human decisions
   remain separate. A material change after approval requires a new decision on the
   changed content. Without approval, keep the currently adopted version in force.

7. **Activate and record adoption.** Under that approval, drain or safely cancel and
   reconcile in-flight work before changing bindings. Preserve monotonic grant use,
   budgets, fencing and publication history; UNKNOWN effects need reconciliation before
   another mutation. Verify resulting pins, instruction digests and policy/runtime
   bindings, perform the approved smoke checks, then record the activated version,
   effective time, responsible owner decision reference, exact artifacts, test evidence
   and recovery point. Revalidate live authority immediately before any effect. Loading
   a resume projection does not renew grants. Record failed activation and stop affected
   work instead of silently falling back or resetting counters.

## Minimal separate adoption record

Use a project-controlled record with references to the approved consumer PR, exact
source/package digest, schema/profile/instruction/runtime/adapter/policy pins, tests,
owner decision, effective time, previous adoption and reconciliation/recovery status.
An evaluation record and an active adoption record are distinct. Reference existing
authoritative task, authorization and effect records rather than copying permissions.

This is documentary guidance, not a new AGENTOPS/1 contract or an instruction to add
fields to the closed ProjectConfig schema. That inactive template remains disabled.
Documentary adoption does not enable an executor. Operational activation requires a
separately implemented and approved runtime/configuration profile with its own evidence.

## Stop and rollback boundaries

| Condition | Required response |
| --- | --- |
| Source, digest, provenance or required pin is missing | Stop the affected update and resolve it through the trusted channel |
| Old reader rejects the candidate or required profile is unsupported | Keep the active version; prepare negotiated migration or defer adoption |
| Tests fail or privacy/compatibility issue is blocking | Preserve findings, repair/review the candidate or decline the update |
| Owner approval is absent or no longer matches the content | Keep the active adoption; request a decision on the exact reviewed content |
| Effect or state is uncertain during activation | Stop affected effects; reconcile using original identities and authoritative records |
| Approved rollback is needed | Restore compatible code/instruction pins while retaining current consumption, fences and effect history; validate before reactivation |

Never restore an old ledger merely to match old code. If safe rollback or migration
is not demonstrated, use a reviewed recovery plan and stop affected execution. Record
the outcome; a merged consumer PR alone does not prove activation or conformance.

See [distribution](DISTRIBUTION.md), [compatibility](../AGENTOPS_COMPATIBILITY_REPORT.md),
[conformance](CONFORMANCE.md) and the [resume template](../templates/project/RESUME.md).
