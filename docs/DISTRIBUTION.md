# Distribution and consumer adoption

The initial public source candidate is `0.1.0-draft.1`; the wire draft is AGENTOPS/1.
No remote release or tag is created by this directory. Package, protocol, schema
catalog, runtime, executor binding and consumer policy versions are distinct.

Use immutable release content, source commit and artifact digests. Public schema
IDs in this candidate use a reserved example catalog and offline resolution; they
are not endpoints. A future production namespace requires a reviewed release and
migration, not a silent rewrite of published IDs.

PATCH changes do not alter accepted data, authority or observable behavior. MINOR
changes add negotiated compatible profiles/catalogs. MAJOR changes break existing
contracts or semantics. Draft status does not waive review. Strict readers can
reject a new field, so additive syntax is not automatically compatible.

A release requires maintainer approval of exact content, privacy and license review,
tests, compatibility/migration analysis and known limitations. Publish only the
allowlisted files; regenerate and verify manifests and artifact digests. Never
publish a development directory or source history wholesale.

Consumers pin the standard, instructions, runtime and policy by version/digest.
A release notification proposes an update; it does not install code, change prompts,
expand permissions, alter a model, renew grants or relaunch old tasks. Consumer
owners approve a diff, tests, migration, backup and activation record.

Drain/reconcile work before changing versions. Rollback must preserve monotonic
consumption, fencing and publication history; restoring an old ledger can duplicate
effects or reuse grants. If safe reversal is unknown, stop and obtain a reviewed
recovery plan. Administrative and production operations need separate authorization.
