# Offline schema catalog

There are fourteen primary contracts, common definitions, and one deliberately
inactive project configuration schema. Catalog IDs use the reserved example domain
`schemas.example.org`; the validator registers local files and has no network
retrieval fallback. These IDs are not hosted endpoints.

`examples/index.json` names the expected positive/negative outcome and schema for
each synthetic fixture. Positive means structural validity in the reference profile,
not real credentials, authority or evidence from a live platform. Illustrative
registry/policy digests do not certify an external identity. Negative values are
synthetic and cannot authorize operations.

The reference demo builds a correlated synthetic chain and computes its bundle
digest from exact serialized bytes. The EXAMPLE-HANDOFF/1 fixture is a synthetic
message format for preservation tests; no external protocol compatibility is claimed.
No original project artifact or account is needed to run the suite.

Native contracts reject extra fields and unknown versions. Semantic guards cover
selected scope, revision, lease, authorization, budget and closure relationships.
Authentication, real grant issuance and exhaustive artifact verification belong to
a future reviewed operational implementation. See docs/spec/1/SPECIFICATION.md
and docs/CONFORMANCE.md for the format profile and limits.
