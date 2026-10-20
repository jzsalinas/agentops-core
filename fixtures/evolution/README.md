# Fictional evolution fixtures

All inputs are newly constructed fictional data. Dates, identifiers, observation
classes and probe results describe simulations, not historical or live operations.

| Fixture | Purpose |
| --- | --- |
| effect-plan.json / publication-body.txt | Proposed plan for one exact fictional report effect |
| effect-cases.json | Base simulated trusted facts and 19 valid/invalid decision variations |
| evidence-acceptance.json | Two criterion assertions; digest and procedure/source/revision binding |
| observation-wide.json / observation-narrow.json | PASS with correct or incorrect condition; preserve valid partial coverage |
| evidence-cases.json | Explicit expected coverage for both observation artifacts |
| destination-projection.json / inventory.json | Two destinations, selected/foreign rows, nested excluded fields and nonfunctional canaries |
| bundle.json / contract-records.json | Existing AGENTOPS/1 envelopes with actual artifact lengths/digests and linked request/handoff/incident/recovery |

`agentops_reference/profile_checks.py` contains selected pure predicates for these
experiments. It is neither a general profile validator nor a runtime. The test harness
supplies simulated trusted facts/policy; native structural validity alone cannot
authenticate them. Additional adversarial mutations in tests cover drift, false
coverage, forbidden links, malformed values, consumed grants and closed-contract limits.

Run `python3 -B -m unittest discover -s tests -p test_evolution_profiles.py -v` or
the complete `python3 -B tools/check.py`. No network, UI, model, service, durable
worker or actual publication is exercised. See the test report for scope and counts.
