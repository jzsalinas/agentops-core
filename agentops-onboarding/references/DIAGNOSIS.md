# Read-only diagnosis

Use the scope given by the owner. Read the host's existing instruction hierarchy
first, including nested instructions that apply to files being inspected. Resolve
and read their referenced policies sequentially before reading other project files;
if unavailable, report the gap before continuing any dependent inspection. Do not
bypass existing policy by creating an override. Limit file count and byte reads to
the goal; a suggested initial bound is 30 relevant text files of 64 KiB each.
Apply the initial bound per assessed project, and state the aggregate when assessing
several projects. Report truncated or skipped material. Do not traverse symlinks, ignored dependency
trees, secret stores or operational logs. If a needed fact would require execution
or access outside scope, report it as unknown and propose a later authorized check.

Record observations and source references for:

| Inspect | Decision informed |
| --- | --- |
| Language/framework declarations and source layout | Relevant guidance and ownership boundaries |
| Root, nested and tool-specific agent instructions | Applicable authority, scope and safe append location |
| Test configuration and development documentation | Proposed local validation, never an automatic run |
| Dependency manifests and declared external repositories/processes | Trust boundaries, unavailable evidence and costs |
| Existing permissions, approval and evidence policies | Controls to reuse; incompatible requirements |
| Team structure and actual independent tasks | Whether delegation provides any benefit |
| Existing recovery, decision and adoption records | Reuse mechanisms rather than add a ledger |

Do not infer production access, authorization or live dependency state from a
manifest. Do not ask for credentials. A multi-team organization alone does not
justify multiple agents or a runtime. A small project may need only clearer scope
and review instructions, or no AgentOps changes at all.

Treat source provenance separately from relevance. If the source is only a draft
branch, an unsigned asset without a trusted digest, an inaccessible release channel
or a policy conflict, continue diagnosis and mark adoption deferred. An offline
project can use an already authenticated, locally available publication; absence
of such evidence must remain unknown. Declined adoption ends onboarding without
changes. Continue any unrelated requested work under the current project policy.
