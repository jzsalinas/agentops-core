# SPDX-License-Identifier: MIT
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from jsonschema import ValidationError
from agentops_reference.contracts import registry, validate_contract, validate_semantics, guard_execution
ROOT=Path(__file__).resolve().parents[1]

class ContractsTest(unittest.TestCase):
    def setUp(self):
        self.graph=json.loads((ROOT/'fixtures/contract-graph.json').read_text())

    def test_schemas_and_all_examples_offline(self):
        with patch('socket.socket',side_effect=AssertionError('Network forbidden')):
            registry()
            index=json.loads((ROOT/'schemas/1/examples/index.json').read_text())
            for case in index:
                with self.subTest(path=case['path']):
                    value=json.loads((ROOT/'schemas/1'/case['path']).read_text())
                    if case['valid']:validate_contract(value,case['schema'].split('.')[0])
                    else:
                        with self.assertRaises(ValidationError):validate_contract(value,case['schema'].split('.')[0])

    def test_semantic_valid_graph(self):
        for value in self.graph.values():validate_semantics(value)
        self.assertTrue(self.guard())

    def guard(self,**kwargs):
        g=self.graph
        return guard_execution(g['Task'],g['Execution'],g['TaskAssignment'],g['Authorization'],kwargs.get('now','2025-01-01T12:01:00Z'),kwargs.get('attempt',1),kwargs.get('fence',1))

    def test_expired_authorization(self):
        with self.assertRaises(ValueError):self.guard(now='2025-01-01T12:21:00Z')

    def test_lease_expired(self):
        self.graph['TaskAssignment']['lease_expires_at']='2025-01-01T12:00:30Z'
        with self.assertRaises(ValueError):self.guard()

    def test_attempt_budget_exhausted(self):
        with self.assertRaises(ValueError):self.guard(attempt=3)

    def test_fenced_late_result(self):
        with self.assertRaises(ValueError):self.guard(fence=2)

    def test_sha_drift(self):
        self.graph['Task']['resource']['revision']='b'*40
        with self.assertRaises(ValueError):self.guard()

    def test_policy_changed(self):
        self.graph['Task']['policy_digest']='sha256:'+'b'*64
        with self.assertRaises(ValueError):self.guard()

    def test_cross_project(self):
        self.graph['Execution']['project_id']='urn:agentops:other:project:1'
        with self.assertRaises(ValueError):self.guard()

    def test_grantee_escalation(self):
        self.graph['Authorization']['grantee_agent_id']='urn:agentops:example-project:agent:evil'
        with self.assertRaises(ValueError):self.guard()

    def test_budget_escalation(self):
        self.graph['Execution']['budget']['max_tokens']=100
        with self.assertRaises(ValueError):self.guard()

    def test_consumed_grant(self):
        self.graph['Authorization'].update(status='CONSUMED',used_count=2)
        with self.assertRaises(ValueError):self.guard()

    def test_cannot_execute_unknown_revision(self):
        self.graph['Task']['resource'].update(revision=None,revision_status='UNKNOWN')
        with self.assertRaises(ValueError):self.guard()

    def test_invalid_semantic_cases(self):
        cases=[]
        v=copy.deepcopy(self.graph['Authorization']);v['expires_at']=v['valid_from'];cases.append(v)
        v=copy.deepcopy(self.graph['Authorization']);v['used_count']=3;cases.append(v)
        v=copy.deepcopy(self.graph['ApprovalRequest']);v['status']='APPROVED';cases.append(v)
        v=copy.deepcopy(self.graph['ExecutionAttempt']);v['ended_at']=None;cases.append(v)
        v=copy.deepcopy(self.graph['EvidenceBundle']);v['claims_not_supported']=v['claims_supported'];cases.append(v)
        for v in cases:
            with self.subTest(kind=v['kind']):
                with self.assertRaises(ValueError):validate_semantics(v)

    def test_terminal_or_cancelled_execution_not_restarted(self):
        self.graph['Execution']['status']='SUCCEEDED'
        with self.assertRaises(ValueError):self.guard()
        self.graph['Execution']['status']='CLAIMED';self.graph['Execution']['cancel_requested']=True
        with self.assertRaises(ValueError):self.guard()

    def test_publication_request_without_exact_digest_rejected(self):
        v=copy.deepcopy(self.graph['ApprovalRequest']);v['scope']['artifact_digests']=[]
        with self.assertRaises(ValidationError):validate_contract(v)

    def test_invalid_closure_or_self_review_rejected(self):
        t=copy.deepcopy(self.graph['Task']);t['states']['closure']='CLOSED'
        with self.assertRaises(ValueError):validate_semantics(t)
        t=copy.deepcopy(self.graph['Task']);t['review_target']=t['target']
        with self.assertRaises(ValueError):validate_semantics(t)
