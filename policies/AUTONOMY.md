# Generic autonomy policy

This policy describes boundaries; it does not grant any agent access. Project
configuration starts disabled and must be adopted by authorized project owners.

AUTONOMOUS: reversible local analysis of explicitly allowed synthetic or authorized
inputs, schema validation, isolated tests, documentation, and preparation of evidence.
The default reference profile never executes repository-controlled code or contacts
a model, person, remote service, or production system.

APPROVAL_REQUIRED: any external publication, paid inference, transfer of private
context, or personal-resource operation unless covered by an existing explicit,
current, scoped delegation. Prepare exact resources, bytes/digests, effects,
preconditions, time window, budget, and validation before requesting a missing decision.

CRITICAL_APPROVAL: merging, deployment, changing permissions or secrets, deleting
resources, and production operations. These require separate authorization and are
outside the reference profile.

A parent may delegate only a subset of its resources, actions, budget, and deadline.
Subagents cannot approve each other, renew authority, or reset aggregate limits.
Technical capability, credential possession, and human authorization are separate.
Silence never grants approval. New standard versions never silently renew grants.
