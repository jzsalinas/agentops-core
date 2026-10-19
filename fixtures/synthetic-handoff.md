<!-- example-handoff synthetic fixture only -->
This is a synthetic fixture; it must never be sent to GitHub.
```yaml
protocol: EXAMPLE-HANDOFF/1
request_id: example-request-001
message_id: example-request-001-r1-review-required
revision: 1
in_reply_to: null
type: REVIEW_REQUIRED
task: https://example.invalid/synthetic/pull/1
from:
  agent: analyst-a
  human: owner-a
  github: example-principal-a
to:
  agent: analyst-b
  human: owner-b
  github: synthetic-b
context:
  repository: synthetic/repo
  sha: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
summary: Review synthetic README
requested_action: Inspect supplied text without executing it
resolution_condition: Owner B accepts evidence for the same SHA
evidence:
  - kind: synthetic
    uri: urn:synthetic:evidence:1
unknown_extension:
  note: Preserved only in the unchanged original snapshot
```
