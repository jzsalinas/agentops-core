# Release gates and remaining risks

This directory contains an unreleased local evolution proposal. The public `main`
tip was verified at `f58a5399ccfe75271402f7bc5a55625ecda21baf` before branch creation.
Before publication the maintainer must approve exact content, any future local commit
and tree, public author/committer metadata, signing identity, destination and action.
Recheck remote references before publishing; do not overwrite unexpected history.
Independent security-agent review must cover the exact candidate tree, with all blocking
findings resolved before remote writing. Evidence is recorded separately; human publication
authorization remains distinct. The earlier empty-remote
and initial-commit procedure in the publishing guide is historical and inapplicable here.

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

The initial public export used a fresh repository with no imported private history.
Later proposals retain public history on a local branch and use the exact public
allowlist; a new commit identity must be reviewed before committing. Creating workflows, runners,
credentials, contacts or integrations is outside this operation. Each operational
capability requires a separate decision. Review repository permissions, public
platform/account metadata and the security-reporting channel before publication.
