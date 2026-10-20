# Local evolution validation results

Review date: 2026-10-19 (America/Asuncion). Baseline:
`f58a5399ccfe75271402f7bc5a55625ecda21baf`. Scope: offline synthetic checks only.

| Check | Result | Evidence and limits |
| --- | --- | --- |
| Existing baseline suite before edits | PASS: 49 tests, zero failures/errors/skips | `python3 -B tools/check.py`; source matched updated main |
| Added acceptance experiments | PASS: 26 tests, zero failures/errors/skips | `python3 -B -m unittest discover -s tests -p test_evolution_profiles.py -v` |
| Complete final suite | PASS: 75 tests, zero failures/errors/skips | [Machine-readable report](reports/local-tests.json); includes original 49 unchanged tests |
| Existing schemas/examples | PASS: 16 schema files, 16 positive and 20 negative examples | Offline registry; no retrieval fallback |
| Native compatibility and legal notices | PASS: unchanged baseline protected files | All original schemas/examples, five test modules, native validators/guards/reducers, DDL, inactive configuration, dependencies, MIT and third-party notices compared byte for byte |
| Candidate public payload | PASS: zero findings | Existing auditor, clean export and exact index payload, private denylist outside export; [audit report](reports/privacy-audit.json) |
| Public manifest/checksums | PASS | Exact PUBLIC_FILES inventory, bytes, SHA-256 and MANIFEST verified for every candidate file |
| Whitespace and links | PASS | Git diff check and internal-link validation in complete local check |

Environment: Python 3.14.4; jsonschema 4.19.2, referencing 0.36.2, PyYAML 6.0.3,
attrs 25.4.0, jsonschema-specifications 2023.12.1, rpds-py 0.27.1. Dependency pins
are unchanged. Commands use `python3` because this environment has no `python` alias.

The 26 new methods include 19 table-driven effect cases plus adversarial subcases.
They exercise routine versus new-scope dialogue, stricter human/tool rules, pending
asynchronous state, UNKNOWN/readback/no-resend, task/resource/policy/output/destination
drift, grant scope/effect limits, unsupported profiles, exact artifact links, closed
schemas, nullable-metric boundaries, per-criterion relevance, equal bytes under different
names, human versus provider evidence, preserved partial coverage, supersession,
pre-emission field/value selection, synthetic canaries, log/error/bundle channels,
restricted-link export rejection, legitimate summary acceptance and resume revalidation.

Local checks perform zero network requests, model invocations, external business effects
or workflow creation. Updating the remote-tracking baseline was a separate read-only
Git operation, not a test. No remote mutation was performed. Main remains at the base
commit. Local commit preparation is authorized on the evolution branch; any public push
requires a separate decision naming the exact commit. Commit/tree and independent
exact-tree review evidence are recorded separately to avoid self-referential hashes.

The audit uses the original public auditor without weakening any rule, including
hidden-entry rejection. It inspects the clean candidate export and exact staged blobs;
`.git` is excluded from the export rather than allowlisted. Existing attribution is
preserved with the narrowly approved LICENSE exception. Content was reviewed separately;
private source material and the denylist are outside the public inventory/history.

Final passing checks follow correction of an intermediate preparation check whose
new documentation links referenced this not-yet-created report. That was a missing
candidate file, not a failing acceptance test; the final full check includes all links.

A separate security agent identified two publication-preparation issues: the link
count included internal Git metadata, and the public-summary experiment's link rejection
was described too broadly. The checker now excludes `.git`; the report is regenerated
against the exact public payload. Recognized URI/Markdown/HTML forms now have additional
negative subcases, with the incomplete-detection limit stated explicitly. The suite
still contains 75 methods. A universal adoption guide adds one documentary file to the
initial 124-file candidate; final publication review covers all 125 files, including
the allowed hidden files. Exact-tree findings and limitations are retained separately.

These results do not verify a trusted issuer, actual observation provenance, real
dialogue interpretation, live tool/infrastructure output isolation, durable storage,
multiprocess races, crash recovery, provider compatibility, deployment, runtime operation,
or measured efficiency. The runtime fault matrix remains unexecuted/PROPOSED. The
separate agent review is task independence in the same environment, not independent
human or institutional certification. Publication remains withheld until all blocking
findings are resolved and the maintainer authorizes the exact commit.
