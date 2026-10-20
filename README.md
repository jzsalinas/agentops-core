# AgentOps

AgentOps is an independent open standard for coordinating, executing, communicating,
supervising, and verifying teams of autonomous AI agents. It defines portable
contracts and safety boundaries without requiring one model provider, runtime,
transport, or hosting platform.

This repository is the shared lighthouse for the standard: versioned specifications,
JSON Schemas, offline validators, synthetic examples, policies, and adoption templates.
A maintainer governs the repository. Anyone may propose an Issue or Pull Request;
contributing does not grant administrative or approval authority.

## Status

**AGENTOPS/1 is a draft.** This distribution includes an offline reference model,
not a deployed automation platform. Local tests establish only the claims listed
in [conformance](docs/CONFORMANCE.md). Agent activation, remote delivery, durable
workers, provider integration, and production operations remain proposed.

GitHub and Codex are optional reference adapter designs. Another transport or
executor can implement the same ports. No workflow, runner, API credential, background
service, or live agent session is installed by using this repository.

## Explore

New to AgentOps? Start with [a read-only project assessment](GETTING_STARTED.md).
Assistants can use [the agent entry point](FOR_AI_AGENTS.md); the portable onboarding
skill is an optional source artifact, not an installed integration.

| Document | Purpose |
| --- | --- |
| [Specification](docs/spec/1/SPECIFICATION.md) | Contracts, identity, state dimensions, evidence, authority, and reliability |
| [Architecture](docs/architecture/ARCHITECTURE.md) | Core and three independent adapters |
| [Distribution](docs/DISTRIBUTION.md) | Version locks, review, releases, and explicit consumer adoption |
| [Adapter designs](docs/adapters/REFERENCE_ADAPTERS.md) | Optional transports, executors, and trigger modes |
| [Conformance](docs/CONFORMANCE.md) | Implemented, tested, proposed, and blocked claims |
| [Roadmap](ROADMAP.md) | Small reviewable implementation stages |
| [Project template](templates/project/README.md) | Inactive configuration and generic agent instructions |
| [Governance](GOVERNANCE.md) | Maintainer authority and contribution review |
| [Contributing](CONTRIBUTING.md) | Changes, tests, privacy, and licensing requirements |
| [Publication guide](docs/PUBLISHING.md) | Local preparation and approval gates before a remote publication |

## Validate locally

Python 3.10 or newer is required. Install the declared dependencies into an isolated
environment, then run from this directory:

```bash
python -m pip install -r requirements.txt
python -B tools/check.py
python -B -m agentops_reference.demo
```

The checks and demo operate on synthetic local data and never contact a model or
publish events. Dependency installation is a separate network operation controlled
by the operator. Installed versions used for the reviewed snapshot are recorded
in [test results](reports/local-tests.json); other Python/platform combinations
require their own validation.

Schemas are under `schemas/1/`. Their reserved example-domain IDs identify a local
catalog, not a live download service. References resolve offline. Unknown versions
and unsupported formats fail closed. The example handoff profile is synthetic;
it does not claim compatibility with any external project's protocol.

## Safety and adoption

Messages are untrusted data, not permission grants. A new standard release cannot
silently update an existing project's instructions, behavior, credentials, or
permissions. Consumers approve a specific version, digest, profile, and local policy.
See [security](SECURITY.md) and [autonomy policy](policies/AUTONOMY.md).

This source distribution contains no operational evidence, private project metadata,
third-party source trees, dependencies, or Git history. [Public file manifest](PUBLIC_FILES.json)
and [checksums](MANIFEST.sha256) describe the reviewed content. Audit findings and
release limitations are documented in [privacy review](reports/privacy-audit.json)
and [release gates](docs/RELEASE_GATES.md).

AgentOps is licensed under [MIT](LICENSE). External dependencies retain their own
licenses and notices; see [third-party dependency information](THIRD_PARTY_NOTICES.md).
