# Destination evidence projection: optional artifact guide

Candidate artifact profile: `agentops-destination-projection/0.1-experimental`.
See the [projection policy example](../../fixtures/evolution/destination-projection.json)
and [synthetic inventory](../../fixtures/evolution/inventory.json).
Policy comes from the trusted destination owner, never from inventory contents.

Select the authorized resource explicitly before asking a tool for information. At
the adapter boundary filter rows, fields and value shapes before returning to the
model, writing logs, serializing exceptions or attaching evidence. A title, URL or
free-text value can leak context even when its field name is allowlisted. If the
upstream tool has already emitted a broad inventory to the model, downstream redaction
cannot undo that emission. Such a tool needs a narrower API or isolated adapter.

The local example supports only fixed fictional resource IDs and READY/PENDING states.
MODEL_CONTEXT returns resource_id/state, while PUBLIC_SUMMARY returns state only.
Other fields are discarded, including nested objects. Unexpected selected values,
duplicate selectors or unknown destinations fail with a fixed category and no raw
value. No logs or partial result are returned on failure. Real policies may return
authorized opaque IDs or aggregate categories/counts, but even counts need destination
approval. This example intentionally exposes neither rejected values nor counts.

Keep three separate products: restricted operational evidence; a local finding with
its provenance under the same access controls; and a new public synthetic lesson.
No automatic export of either earlier product is allowed. Public text links only to
public contracts and fictional examples, excludes source paths/identifiers, and has
an explicit file manifest plus independent content review before publication.

Use Incident category PRIVACY and RecoveryAction for failures. Record cause only when
supported; otherwise preserve UNKNOWN. Redactions describes removed categories, never
copies the removed value. A synthetic public incident illustrates the contract without
copying an operational record. Recovery cannot claim to reverse an already emitted value.

Run the existing public auditor with a maintainer-controlled private denylist outside
the export. Check exact file bytes and decoded structured strings, hidden entries and
metadata. The auditor is additional defense: reserved example domains are suitable for
fictional examples but do not automatically make any link public or its content safe.
The local public-summary experiment rejects recognized absolute URI, network-path,
Markdown destination and HTML link forms, including FTP, mailto and internal-reference
schemes. It is not a complete detector of encoded or rendered links. General prose
still needs human privacy review for relationships and encodings a scanner cannot detect.

Tests capture return values, stdout, stderr and exceptions from the synthetic projector,
and inspect a generated bundle. No real tool backend or infrastructure logging path is
covered. Integration must verify every such channel before claiming pre-emission safety.
