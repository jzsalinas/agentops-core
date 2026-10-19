# Release gates and remaining risks

This directory is a reviewed source candidate. The official public repository
already exists and its empty state and `main` target were checked during local
preparation. This does not authorize a push. Before publication the maintainer must
approve the exact local commit and tree, public author/committer metadata, any
signing identity, destination and initial draft scope. Recheck remote references
before publishing; do not overwrite an unexpected remote history.

The MIT notice is approved for this candidate. Do not infer a legal identity or
administrative permission from other files. Dependency software is not bundled;
its own copyright notices and licenses must remain intact when separately installed.
Future vendoring or media requires another license/privacy review.

Known implementation limits remain: the standard is draft; the reference is offline;
URI/timestamp checking is a conservative profile; persistent workers, real provider
integration, races, crash recovery, authority issuance and remote publication have
not been established by the local suite. Pinned dependencies still need normal
ongoing maintenance and vulnerability review. Only the recorded interpreter/environment
was tested; installation on a new platform needs validation.

A lexical audit cannot establish the absence of every possible personal identifier
or prove title to every contribution. Review prose, fixtures, hidden files, generated
content and archive metadata, using a private project-specific denylist in addition
to generic checks. Never include that denylist or private provenance in a release.

Local preparation uses a new repository with no imported history, the exact public
allowlist and an explicitly approved public commit identity. Its first commit is
held locally until final publication approval. Creating workflows, runners,
credentials, contacts or integrations is outside this operation. Each operational
capability requires a separate decision. Review repository permissions, public
platform/account metadata and the security-reporting channel before publication.
