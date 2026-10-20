# From a link to reviewed instructions

A developer supplies the official source link and the assessment request from
[GETTING_STARTED.md](GETTING_STARTED.md). The assistant reads the entry guide and
skill manually. It states what it actually read; no host installation is implied.

The assistant reads applicable instructions and a bounded selection of project
files. It describes stack, tests, risks and equivalent controls with references.
For a single developer it may propose one short scope/evidence convention. For
several teams it first checks whether their existing review and ownership process
already solves the coordination problem. A request for autonomy does not enlarge
permissions or require delegated agents.

The assistant returns a minimal patch in the conversation, preserving existing
instructions, plus an explicit publication/trust gate. If only an unpublished draft
exists, the patch is contingent and cannot be adopted. If an authenticated published
prerelease exists, its status and risks are stated and owner acceptance is required.
Offline evaluation uses available project evidence and clearly marks unavailable
release evidence. No ordinary development task waits on a network outage.

The owner can decline, defer, narrow the scope or approve the exact documentary
diff and immutable source. Only approval permits applying those changes. The
assistant then verifies the diff, pins and local guidance references and records
the decision using the existing project mechanism. The short snippet points future
sessions to that policy and selected guidance. It does not replace either one.

A future session loads instructions according to its own host's precedence rules.
It verifies the selected local guidance and current permissions/evidence policy.
It checks for updates only if that project separately adopted a supported Update
Discovery profile. Unapproved or unverifiable updates leave active pins unchanged.
No source push updates consumers. Runtime activation and service access require
their own proposal, evidence and authorization.

The owner may separately approve installing the portable skill in the current
host's project discovery directory. That is optional: manual document use remains
valid. A real loading check is required before claiming automatic discovery, and
does not prove another host will discover the same folder.
