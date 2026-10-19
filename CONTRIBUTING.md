# Contributing

Submit an Issue for discussion or a Pull Request with a concrete problem, intended
behavior, compatibility analysis, relevant tests, and any migration steps. Use only
generic identities and synthetic data, such as `team-a`, `team-b`, `agent-reviewer`,
`example-project`, and reserved example domains.

Do not submit customer records, names of private collaborators, personal contacts,
credentials, device paths, real resource identifiers, historical operational logs,
or identifying discovery material. A checksum or screenshot can disclose provenance;
review metadata and packaged content as carefully as visible prose.

Contributions must be material you are authorized to submit under the project MIT
license. Identify external material and its license before adding it. Preserve
legally required notices. If required attribution conflicts with the distribution's
privacy policy, exclude the resource or obtain an approved alternative; never
remove someone else's copyright notice to conceal identity.

Run `python -B tools/check.py` and the privacy auditor. Add meaningful cases for
changed behavior. Negative fixtures must use synthetic, unmistakably nonfunctional
values rather than realistic credentials or private identifiers. Do not weaken
assertions merely to make a test pass.

A new field can break strict readers. Analyze schema, validator, instructions,
provider assumptions, and consumer policy impacts together. Do not rewrite published
schema IDs in place. A contribution may propose an adapter, but must not quietly
introduce automatic activation, dependency updates, or external side effects.

The maintainer reviews and approves changes. A contribution is not a grant of
administrative or approval authority. No live workflow or remote publication is
part of this initial source distribution.
