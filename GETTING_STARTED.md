# Start with an assessment

Give your assistant the official repository link supplied by the maintainer and
this request:

> Read GETTING_STARTED.md and FOR_AI_AGENTS.md at this source. Assess this project
> for an optional AgentOps adoption, using read-only inspection. Respect existing
> instructions and equivalent controls. Report findings, a minimal proposed diff,
> publication/trust evidence, costs and limitations. Do not install anything,
> overwrite instructions, run project commands or activate services. Wait for my
> approval of the exact proposal before changing this project.

No runtime, credentials, CI, multiple agents or infrastructure are needed for the
assessment. A link supplies material to evaluate; it does not install a skill or
grant the source authority over your project.

1. **Discover:** read the introduction and identify the source and publication
   channel approved by the project owner.
2. **Evaluate:** inspect the project and existing instructions without changing
   files. A small project may need only its existing workflow.
3. **Prepare:** receive a concrete proposed patch, selected guidance, immutable
   source pins, trust evidence and validation plan. Missing evidence stays unknown.
4. **Approve:** review the exact files, pins, scope and any prerelease acceptance.
   Declining is a complete, valid outcome.
5. **Adopt:** only after approval, apply the reviewed documentary patch, preserve
   existing instructions and record the approved source in the project's existing
   decision mechanism. Review the resulting diff before use.
6. **Activate:** separately authorize and validate any operational implementation.
   Documentary adoption provides instructions, not workers or durable guarantees.

Use only an officially published, verifiable release from the configured channel.
Pin its version, source commit and artifact digest; authenticate the digest through
an independently adopted trust anchor. An unauthenticated checksum beside an asset
is insufficient. A published prerelease needs explicit owner acceptance. A draft
on a branch or PR is evaluation material, not an eligible release. If no release
can be verified, prepare a contingent proposal and continue ordinary project work.
Never select the moving head of `main` as an installed dependency.

The [portable skill](agentops-onboarding/SKILL.md) can be read manually. It is not
installed by this checkout. After review, an owner may approve a project-scoped
copy into their tool's documented discovery directory; see the [compatibility
matrix](AGENTOPS_ONBOARDING_COMPATIBILITY.md). Preserve the [MIT notice](LICENSE)
with redistributed material. Installation and host discovery are separate checks.

See the [journey](AGENTOPS_ONBOARDING_USER_JOURNEY.md), [proposed persistent
snippet](agentops-onboarding/assets/AGENTS_SNIPPET.md) and [adoption
checklist](agentops-onboarding/assets/ADOPTION_CHECKLIST.md). No consumer project is
modified by this kit.
