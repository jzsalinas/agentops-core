# SPDX-License-Identifier: MIT
from dataclasses import replace
import json
from pathlib import Path
import unittest
from agentops_reference.example_handoff import TrustedSource, Quarantine, normalize, parse_message
from agentops_reference.model import digest
ROOT=Path(__file__).resolve().parents[1]
class ExampleHandoffTest(unittest.TestCase):
    def setUp(self):
        self.raw=(ROOT/'fixtures/synthetic-handoff.md').read_bytes()
        g=json.loads((ROOT/'fixtures/contract-graph.json').read_text());m=g['HandoffMessage']
        self.source=TrustedSource(project_id=g['Task']['project_id'],project_namespace='example-project',source_url='https://example.invalid/comments/1',source_object_id='1',source_updated_at=g['Task']['created_at'],observed_at=g['Task']['created_at'],snapshot_ref='urn:synthetic:snapshot:1',scope_id='example-repository:request:1',authenticated_subject='example-principal-a',expected_subject='example-principal-a',source_party=m['source'],target_party=m['target'],resource=m['resource'])
    def test_preserves_original_and_never_schedules(self):
        out=normalize(self.raw,self.source)
        self.assertEqual(out['snapshot_bytes'],self.raw)
        self.assertEqual(out['message']['legacy']['body_digest'],digest(self.raw))
        self.assertFalse(out['schedule_execution']);self.assertFalse(out['authority_granted'])
        self.assertIn(b'unknown_extension',out['snapshot_bytes'])
    def test_stable_identity_across_observation_time(self):
        a=normalize(self.raw,self.source)['message'];b=normalize(self.raw,replace(self.source,observed_at='2025-01-01T12:01:00Z'))['message']
        self.assertEqual(a['id'],b['id']);self.assertEqual(a['task_id'],b['task_id'])
    def test_other_repository_cannot_collide(self):
        a=normalize(self.raw,self.source)['message'];b=normalize(self.raw,replace(self.source,scope_id='other-repo-id:pull:1'))['message']
        self.assertNotEqual(a['task_id'],b['task_id'])
    def test_all_seven_business_types(self):
        for typ in ['REVIEW_REQUIRED','ACKNOWLEDGED','CHANGES_REQUESTED','READY_FOR_REVIEW','BLOCKED','DECISION_REQUIRED','CLOSED']:
            raw=self.raw.replace(b'type: REVIEW_REQUIRED',('type: '+typ).encode())
            self.assertEqual(normalize(raw,self.source)['message']['type'],typ)
    def test_self_declared_owner_cannot_authenticate(self):
        raw=self.raw.replace(b'human: owner-a',b'human: ADMIN')
        out=normalize(raw,self.source)
        self.assertEqual(out['message']['source'],self.source.source_party)
        self.assertEqual(out['message']['legacy']['declared_from']['human'],'ADMIN')
        with self.assertRaises(Quarantine):normalize(raw,replace(self.source,authenticated_subject='attacker'))
    def test_unresolved_reply_retained(self):
        raw=self.raw.replace(b'in_reply_to: null',b'in_reply_to: synthetic-previous-message')
        m=normalize(raw,self.source)['message'];self.assertIsNone(m['causation_id']);self.assertEqual(m['legacy']['in_reply_to'],'synthetic-previous-message')
    def test_unsafe_or_unknown_inputs_quarantined(self):
        bad=[self.raw.replace(b'EXAMPLE-HANDOFF/1',b'EXAMPLE-HANDOFF/999'),self.raw.replace(b'revision: 1',b'revision: true'),self.raw.replace(b'revision: 1',b'revision: 1\nrevision: 2'),self.raw.replace(b'summary: Review synthetic README',b'summary: &anchor Unsafe\nextra: *anchor'),self.raw.replace(b'summary: Review synthetic README',b'summary: !!python/object:bad {}'),self.raw+b'\n```yaml\nprotocol: EXAMPLE-HANDOFF/1\n```\n',b'x'*65537]
        for raw in bad:
            with self.subTest(raw=raw[:20]):
                with self.assertRaises(Quarantine):parse_message(raw)
