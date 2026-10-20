# SPDX-License-Identifier: MIT
"""Offline synthetic acceptance experiments, not operational conformance tests."""
import copy
import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import unittest
from unittest.mock import patch
from jsonschema import ValidationError

from agentops_reference.contracts import guard_execution, validate_contract, validate_semantics
from agentops_reference.model import digest, publication_outcome
from agentops_reference.profile_checks import (
    criterion_outcomes, effect_decision, project_inventory, public_summary_allowed,
)
from tools.audit_public import inspect_files

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'fixtures' / 'evolution'


def load(name):
    return json.loads((FIXTURES / name).read_text())


class EvolutionProfilesTest(unittest.TestCase):
    def setUp(self):
        self.records = load('contract-records.json')
        self.plan = load('effect-plan.json')
        self.acceptance = load('evidence-acceptance.json')
        self.observation = load('observation-wide.json')

    def guard(self, records=None):
        r = records or self.records
        return guard_execution(r['Task'], r['Execution'], r['TaskAssignment'],
                               r['Authorization'], '2025-01-01T12:01:00Z', fence=1)

    def outcomes(self, observation=None, profile=None, revision=None):
        p = copy.deepcopy(profile or self.acceptance)
        raw = (json.dumps(observation).encode() if observation is not None
               else (FIXTURES / 'observation-wide.json').read_bytes())
        for a in p['assertions']:
            a['artifact_digest'] = digest(raw)
        return criterion_outcomes(p, {'observation-wide.json': raw},
                                  subject_revision=revision or 'a' * 40)

    def test_native_records_remain_valid_offline(self):
        with patch('socket.socket', side_effect=AssertionError('Network forbidden')):
            for record in self.records.values():
                validate_semantics(record)
            self.assertTrue(self.guard())

    def test_exact_native_artifact_envelopes_and_references(self):
        bundle = self.records['EvidenceBundle']
        self.assertEqual(bundle, load('bundle.json'))
        for artifact in bundle['artifacts']:
            raw = (FIXTURES / artifact['uri'].rsplit('/', 1)[1]).read_bytes()
            self.assertEqual((artifact['digest'], artifact['bytes']), (digest(raw), len(raw)))
        ref = {'bundle_id': bundle['id'], 'digest': digest((FIXTURES / 'bundle.json').read_bytes())}
        self.assertEqual(self.records['ApprovalRequest']['prepared_bundle'], ref)
        self.assertEqual(self.records['HandoffMessage']['evidence_refs'], [ref])
        grant_digests = self.records['Authorization']['scope']['artifact_digests']
        self.assertIn(digest((FIXTURES / 'effect-plan.json').read_bytes()), grant_digests)
        self.assertIn(digest((FIXTURES / 'publication-body.txt').read_bytes()), grant_digests)

    def test_native_closed_contracts_reject_proposed_inline_fields(self):
        for kind, field in [('Authorization', 'effect_plan'), ('EvidenceBundle', 'assertions'),
                            ('HandoffMessage', 'checkpoint'), ('Incident', 'destination_policy')]:
            value = copy.deepcopy(self.records[kind])
            value[field] = {}
            with self.subTest(kind=kind), self.assertRaises(ValidationError):
                validate_contract(value)

    def test_scope_does_not_gain_arbitrary_effects(self):
        value = copy.deepcopy(self.records['Authorization'])
        value['scope']['actions'] = ['deploy_application']
        with self.assertRaises(ValidationError):
            validate_contract(value)

    def test_native_unknown_metrics_boundary(self):
        value = json.loads((ROOT / 'fixtures/contract-graph.json').read_text())['ExecutionAttempt']
        value['metrics']['tokens'] = value['metrics']['cost_minor'] = None
        validate_contract(value)
        for field in ('wall_seconds', 'external_effects'):
            invalid = copy.deepcopy(value)
            invalid['metrics'][field] = None
            with self.subTest(field=field), self.assertRaises(ValidationError):
                validate_contract(invalid)

    def test_effect_valid_and_invalid_decision_fixtures(self):
        table = load('effect-cases.json')
        self.assertTrue(self.guard())
        for case in table['cases']:
            facts = copy.deepcopy(table['base_facts'])
            facts.update(case['facts'])
            constraints = copy.deepcopy(table['base_constraints'])
            constraints.update(case['constraints'])
            with self.subTest(case=case['name']):
                self.assertEqual(effect_decision(self.plan, facts, constraints), case['expected'])

    def test_unknown_effect_profile_cannot_schedule(self):
        table = load('effect-cases.json')
        self.plan['profile'] = 'unadopted-profile'
        self.assertEqual(effect_decision(self.plan, table['base_facts'], table['base_constraints']), 'STOP_PROFILE')

    def test_delayed_update_then_unknown_then_readback_without_resend(self):
        table = load('effect-cases.json')
        facts, constraints = table['base_facts'], table['base_constraints']
        facts['settled'] = False
        self.assertEqual(effect_decision(self.plan, facts, constraints), 'WAIT_FOR_COMPLETION')
        step = self.plan['steps'][0]
        args = {'body_digest': step['body_digest'], 'target_ref': step['target_ref']}
        state, intent = publication_outcome({}, step['marker'], {}, **args)
        self.assertEqual(intent, 'ONE_SEND_INTENT')
        state, intent = publication_outcome(state, step['marker'], {}, uncertain=True, **args)
        self.assertEqual((intent, state['publication']), ('RECONCILE_ONLY', 'UNKNOWN'))
        facts['prior_effect'] = state['publication']
        self.assertEqual(effect_decision(self.plan, facts, constraints), 'RECONCILE_ONLY')
        state, intent = publication_outcome(state, step['marker'], {step['marker']: args}, **args)
        self.assertEqual((intent, state['publication']), ('NO_SEND', 'CONFIRMED'))
        facts['prior_effect'] = state['publication']
        self.assertEqual(effect_decision(self.plan, facts, constraints), 'NO_ACTION')

    def test_evidence_positive_and_wrong_condition_fixtures(self):
        for case in load('evidence-cases.json'):
            with self.subTest(case=case['name']):
                observed = load(case['artifact'])
                self.assertEqual(self.outcomes(observed), case['expected'])

    def test_renamed_same_bytes_do_not_prove_different_conditions(self):
        p = copy.deepcopy(self.acceptance)
        raw = (FIXTURES / 'observation-wide.json').read_bytes()
        p['assertions'][1].update(artifact_key='renamed.json', condition={'field': 'layout', 'equals': 'narrow'})
        outcomes = criterion_outcomes(p, {'observation-wide.json': raw, 'renamed.json': raw}, subject_revision='a' * 40)
        self.assertEqual(outcomes['layout-wide'], 'SUPPORTED')
        self.assertEqual(outcomes['height-correct'], 'UNSUPPORTED_CONDITION')

    def test_digest_or_missing_artifact_rejects_coverage(self):
        for observations in ({}, {'observation-wide.json': b'changed fictional observation'}):
            result = criterion_outcomes(self.acceptance, observations, subject_revision='a' * 40)
            self.assertEqual(set(result.values()), {'UNSUPPORTED_INTEGRITY'})

    def test_changed_subject_revision_rejects_acceptance(self):
        self.assertEqual(set(self.outcomes(revision='b' * 40).values()), {'UNSUPPORTED_CONDITION'})

    def test_human_report_is_not_provider_observation(self):
        self.observation['source_class'] = 'HUMAN_REPORT'
        p = copy.deepcopy(self.acceptance)
        for a in p['assertions']:
            a['required_class'] = 'PLATFORM_OBSERVATION'
        self.assertEqual(set(self.outcomes(self.observation, profile=p).values()), {'UNSUPPORTED_CONDITION'})

    def test_pass_and_recorded_assertion_cannot_override_observed_condition(self):
        self.observation['conditions']['layout'] = 'narrow'
        self.assertEqual(self.observation['process_result'], 'PASS')
        self.assertEqual(self.acceptance['assertions'][0]['recorded_result'], 'PASS')
        result = self.outcomes(self.observation)
        self.assertEqual(result['layout-wide'], 'UNSUPPORTED_CONDITION')
        self.assertEqual(result['height-correct'], 'SUPPORTED')

    def test_procedure_and_producer_mismatch_reject_coverage(self):
        for field in ('producer', 'procedure', 'subject_id'):
            observed = copy.deepcopy(self.observation)
            observed[field] = 'different-synthetic-source'
            with self.subTest(field=field):
                self.assertEqual(set(self.outcomes(observed).values()), {'UNSUPPORTED_CONDITION'})

    def test_corrected_evidence_links_successor_without_rewriting_original(self):
        before = (FIXTURES / 'bundle.json').read_bytes()
        previous = load('bundle.json')
        successor = copy.deepcopy(previous)
        successor['id'] = 'urn:agentops:example-project:evidence:2'
        successor['supersedes_ids'] = [previous['id']]
        successor['claims_supported'] = ['Corrected fictional observation attached']
        validate_semantics(successor)
        self.assertEqual(successor['record_revision'], 1)
        self.assertEqual((FIXTURES / 'bundle.json').read_bytes(), before)

    def test_unknown_acceptance_profile_is_not_adopted(self):
        self.acceptance['profile'] = 'unadopted-profile'
        with self.assertRaisesRegex(ValueError, '^PROFILE_UNSUPPORTED$'):
            self.outcomes()

    def test_projection_policy_example_matches_selected_output(self):
        policy = load('destination-projection.json')
        rows = load('inventory.json')
        expected = {'MODEL_CONTEXT': {'resource_id': 'resource-allowed', 'state': 'READY'},
                    'PUBLIC_SUMMARY': {'state': 'READY'}}
        for destination, fields in policy['destinations'].items():
            output = project_inventory(rows, selector=policy['selector'], destination=destination)
            self.assertEqual(output, expected[destination])
            self.assertEqual(set(output), set(fields))

    def test_projection_canaries_absent_from_output_logs_errors_and_bundle(self):
        rows = load('inventory.json')
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr), self.assertNoLogs():
            output = project_inventory(rows, selector='resource-allowed', destination='MODEL_CONTEXT')
            rows[0]['state'] = rows[0]['title']
            try:
                project_inventory(rows, selector='resource-allowed', destination='MODEL_CONTEXT')
            except ValueError as exc:
                error = str(exc)
        self.assertEqual(error, 'PROJECTION_VALUE_DENIED')
        bundle = copy.deepcopy(self.records['EvidenceBundle'])
        bundle['claims_supported'] = [json.dumps(output)]
        validate_semantics(bundle)
        emitted = json.dumps([output, error, stdout.getvalue(), stderr.getvalue(), bundle])
        for canary in ('synthetic-sensitive-canary', 'synthetic-foreign-canary', 'NONFUNCTIONAL_SYNTHETIC_VALUE'):
            self.assertNotIn(canary, emitted)
        self.assertEqual(stdout.getvalue() + stderr.getvalue(), '')

    def test_projection_rejects_duplicate_missing_and_malformed_selection(self):
        rows = load('inventory.json')
        for invalid in ([], [rows[0], rows[0]], [None], {'rows': rows}):
            with self.subTest(shape=type(invalid).__name__), self.assertRaises(ValueError):
                project_inventory(invalid, selector='resource-allowed', destination='MODEL_CONTEXT')

    def test_projection_rejects_unadopted_destination_and_nested_value(self):
        rows = load('inventory.json')
        with self.assertRaisesRegex(ValueError, '^PROJECTION_POLICY_DENIED$'):
            project_inventory(rows, selector='resource-allowed', destination='UNADOPTED')
        rows[0]['state'] = {'raw': 'synthetic-sensitive-canary'}
        with self.assertRaisesRegex(ValueError, '^PROJECTION_VALUE_DENIED$'):
            project_inventory(rows, selector='resource-allowed', destination='PUBLIC_SUMMARY')

    def test_private_link_export_rejected_without_echoing_link(self):
        link = 'https://example.invalid/' + 'restricted-reference'
        text = 'Fictional finding: ' + link
        self.assertFalse(public_summary_allowed(text))
        other_forms = ['ftp://example.invalid/restricted-reference',
                       'mailto:' + 'synthetic' + '@' + 'example.invalid',
                       'visualize:synthetic-reference', 'project-file:synthetic-reference',
                       'library-file:synthetic-reference', '//example.invalid/reference',
                       '[reference] (restricted-reference.md)', '<a href="restricted-reference.md">text</a>']
        for form in other_forms:
            with self.subTest(form_type=form.split(':')[0]):
                self.assertFalse(public_summary_allowed('Fictional finding: ' + form))
        policy = {'forbidden_patterns': [{'category': 'restricted-link', 'pattern': 'restricted-reference'}]}
        findings = inspect_files({'sample.md': text.encode()}, policy, verify_manifest=False)
        self.assertTrue(any(f['category'] == 'restricted-link' for f in findings))
        self.assertNotIn(link, json.dumps(findings))

    def test_legitimate_synthetic_public_summary_is_allowed(self):
        self.assertTrue(public_summary_allowed('Fictional report: one condition supported; no remote effect claimed.'))

    def test_resume_does_not_renew_consumed_or_revoked_grant(self):
        self.assertTrue(self.guard())
        for status, count in [('CONSUMED', 2), ('REVOKED', 0)]:
            records = copy.deepcopy(self.records)
            records['Authorization'].update(status=status, used_count=count)
            with self.subTest(status=status), self.assertRaises(ValueError):
                self.guard(records)

    def test_resume_reload_detects_changed_policy_or_resource(self):
        for field in ('policy_digest', 'resource'):
            records = copy.deepcopy(self.records)
            if field == 'resource':
                records['Task']['resource']['revision'] = 'b' * 40
            else:
                records['Task']['policy_digest'] = 'sha256:' + 'b' * 64
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.guard(records)

    def test_native_publication_reconciliation_survives_serialized_snapshot(self):
        step = self.plan['steps'][0]
        args = {'body_digest': step['body_digest'], 'target_ref': step['target_ref']}
        state, _ = publication_outcome({}, step['marker'], {}, **args)
        snapshot = json.loads(json.dumps(state))
        resumed, intent = publication_outcome(snapshot, step['marker'], {}, **args)
        self.assertEqual((intent, resumed['publication']), ('RECONCILE_ONLY', 'UNKNOWN'))
        # Serialization tests reference composition, not a durable process restart.
