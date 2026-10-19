# Preparing and publishing the initial commit

The official public GitHub repository has already been created. The initial target
branch is `main`; read-only inspection confirmed an empty remote during preparation.
Use the maintainer-approved destination. Do not create a second repository or add
an automatically generated README, license or initial commit on the server.

Local preparation and remote publication are separate approvals. This guide permits
neither a push nor enabling integrations. Recheck the remote before publication;
if new references appear, stop and review rather than overwrite them.

1. Review release gates, test results, privacy/dependency audit, exact public manifest,
   copyright notice and package digest. Approve the destination and exact content.
2. Confirm that the existing destination is public, its owner/name match the approved
   repository, its default branch is `main`, and it still has no remote references.
   Platform account identity and commit metadata are public independently of files.
3. Work only from this clean directory. Do not copy a parent .git, private review
   directory, archives of development work, credentials, logs or upstream history.
4. Initialize a fresh repository, configure an approved nonpersonal author/committer
   identity, and inspect any signing identity or automated trailers before committing.
5. Stage only the public allowlist. Inspect the staged file list/diff and commit
   metadata. Create the authorized local initial commit with the exact message below.
6. Record its SHA, complete tree, test/audit results, author/committer identity and
   approved remote. Stop before pushing and obtain authorization for that exact
   commit and `main`. Do not enable workflows, Apps, runners, secrets or services.
7. Publish only after that final authorization. Read back the remote commit, tree
   and blobs and compare all paths, file modes, byte lengths and SHA-256 digests
   against the approved local commit and public manifest. A mismatch blocks acceptance.
   Publication of a draft does not create a stable release or verify remote execution.

Local checks before initializing Git:

```bash
python -B tools/check.py
python -B tools/audit_public.py
sha256sum -c MANIFEST.sha256
```

The directory auditor deliberately rejects unapproved hidden entries, including
`.git`. After initialization, audit the exact index/commit blobs with the same
`inspect_files` validator, or export the approved tree into a clean directory and
run the directory auditor there. Inspect Git configuration and commit metadata
separately; never add `.git` to the public file allowlist. Private review outputs
are outside the public tree and must not be staged.

Fresh local initialization, with no inherited history or template hooks:

```bash
git init --template= -b main
: "${AGENTOPS_PUBLIC_COMMIT_NAME:?Choose an approved nonpersonal display name}"
: "${AGENTOPS_PUBLIC_COMMIT_EMAIL:?Choose an approved public commit address}"
git config --local user.name "$AGENTOPS_PUBLIC_COMMIT_NAME"
git config --local user.email "$AGENTOPS_PUBLIC_COMMIT_EMAIL"
git var GIT_AUTHOR_IDENT
git var GIT_COMMITTER_IDENT
```

Inspect both identities, possible environment overrides, signing metadata and staged
content privately. Do not blindly use inherited global Git identity or invent a
personal contact in example configuration. `git add` is deliberately omitted:
staging must use the exact allowlisted paths, never a parent workspace or an
unreviewed `git add .`. The proposed commit message is:

```text
Initial public draft of the AgentOps standard
```

The approved remote can be configured during local preparation. Setting a remote
does not authorize pushing:

```bash
: "${AGENTOPS_APPROVED_REMOTE:?Use the explicitly approved destination}"
git remote add origin "$AGENTOPS_APPROVED_REMOTE"
# STOP: present the exact commit, tree and audit results for final authorization.
```

After explicit authorization for the recorded commit, verify that `HEAD` is still
that SHA and `main` is the intended branch, then publish without force. Read back
the remote contents as described above. Do not treat this guide, remote setup or a
passing check as publication approval. No stable release is part of this procedure.
