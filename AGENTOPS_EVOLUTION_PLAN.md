# Controlled evolution plan

Status: prepared locally for controlled contribution. A local commit is authorized;
push and PR creation require a subsequent exact-commit decision. No service, workflow,
release, tag or public version increment is part of this contribution.

1. Review all five RFC against the fixed baseline. Run the existing suite before edits.
   Preserve native schemas, guards/reducers, DDL, dependency pins and license.
2. Prepare optional [effect](docs/guides/EFFECT_PLAN.md),
   [acceptance](docs/guides/EVIDENCE_ACCEPTANCE.md) and
   [destination](docs/guides/DESTINATION_PROJECTION.md) guides. Add fictional JSON
   artifacts and valid/invalid cases; connect native bundles and requests using existing
   digest-bearing references. Exercise bounded local predicates, not live effects.
3. Add the [resume template](templates/project/RESUME.md), linking authoritative
   contracts. Clarify coordinator/subagent behavior as candidate instructions requiring
   explicit consumer adoption. Keep configuration disabled and the ledger singular.
4. Specify the [persistent runtime experiment](docs/experimental/PERSISTENT_RUNTIME.md).
   Require reproducible multiprocess and crash tests before a future implementation
   can claim the milestone. This branch implements none of that runtime.
5. Run old and new tests, inspect changed prose and examples, apply the public auditor
   with a private denylist outside the export, and regenerate exact public manifests.
   Audit a clean export including hidden entries, never allowlist `.git`. Preserve
   private originals outside the repository and exclude them from commit history.
6. Present the [local PR proposal](docs/EVOLUTION_PR_PROPOSAL.md), compatibility report,
   test results, roadmap state and exact allowlist to the maintainer. Publication and
   consumer activation remain separate subsequent decisions.

## Sequence and exit gates

The documentation/local-fixture stage is reviewable now. Its acceptance establishes
only the bounded claims in the test report. A separate security agent reviews exact
candidate trees and records findings outside the public payload; any blocking finding
prevents publication. No independent human approval is implied. The runtime stage stays PROPOSED until its fault
matrix is executed and independently reviewed. Live provider and transport conformance
need additional evidence even after an isolated persistent experiment succeeds.

The recommended next source candidate is `0.2.0-draft.1`, if the maintainer accepts
the optional profiles and instruction changes. Keep AGENTOPS/1 for existing native
records. No version metadata is incremented here. See the compatibility report for
schema-catalog and future wire-major triggers.

The [universal project adoption guide](docs/PROJECT_ADOPTION.md) prepares the consumer
update process as documentation only. It changes no project or integration.
