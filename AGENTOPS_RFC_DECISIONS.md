# RFC technical decisions proposed to the maintainer

All decisions below are recommendations for this local branch, not maintainer votes.
No public version, wire contract, consumer instruction or operating permission is changed
by preparing the proposal. MIT and existing attribution remain intact.

| RFC | Accepted into candidate | Rejected or unnecessary | Deferred evidence |
| --- | --- | --- | --- |
| 01 | Optional effect-plan guide, same-effect versus new-scope examples, settlement/UNKNOWN tests, instruction additions | New consent authority; bypassing a stricter tool/human rule; fixed UI click script; adding fields to Authorization | Authenticated grant interpretation, atomic reservation and actual asynchronous interface enforcement |
| 02 | Per-criterion observations with procedure, revision, class, limits; retain partial coverage; superseding bundles | PASS as acceptance; hash/filename as proof of content; human report promoted to provider observation; new evidence class | Domain-specific instrumentation, provenance verification and real independent acceptance |
| 03 | Minimal reference-only resume template; freshness and revalidation checklist | Second ledger; embedded transferable grants; stable tool-session handles; changing inactive ProjectConfig | Restart recovery against a durable authoritative store |
| 04 | Experimental specification with objective fault oracles and retained evidence requirements | Calling CLI, synthetic prototype or DDL an operational runtime; runtime release or service deployment in this change | Multiprocess ownership, crash recovery, monotonic grants/budgets/fences and idempotent reconciliation |
| 05 | Field/value projection before all model/log/error/bundle outputs; synthetic privacy fixtures; public manifest review | Filter-after-emission as protection; filename allowlist as content policy; exporting incidents or provenance by default | Real adapter isolation, all output channels, destination policy administration and independent privacy review |

No RFC is accepted wholesale. RFC-04 adds acceptance precision to an existing roadmap
milestone; it is not a newly discovered missing contract. RFC-03 is deliberately limited
to a projection. RFC-01/02/05 are immediate documentation and local experiment candidates,
not verified operational controls or mandatory native protocol extensions.

Expected learning: one operator can race its own pending effect; evidence must observe
the requested condition; current authority must be reloaded rather than remembered;
privacy belongs before emission; operational guarantees require durable implementation.
These are testable hypotheses for future adapters, not quantified benefits.

Publication remains withheld until independent security review has no blocking findings
and the maintainer authorizes the exact commit. Version assignment and explicit consumer
adoption remain separate decisions; a branch push or PR is neither one.
