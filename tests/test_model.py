# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import sqlite3
import unittest
from agentops_reference.model import key,receive,analyze_read_only,publication_outcome,review_signal
ROOT=Path(__file__).resolve().parents[1]
class ModelTest(unittest.TestCase):
    def setUp(self):self.task=json.loads((ROOT/'fixtures/contract-graph.json').read_text())['Task']
    def test_tuple_encoding_has_no_separator_collision(self):self.assertNotEqual(key('a:b','c'),key('a','b:c'))
    def test_replay_delivery_and_business_duplicates(self):
        ledger,status=receive({},'d1','e1','hash1','business1');self.assertEqual(status,'REGISTERED')
        ledger,status=receive(ledger,'d1','e1','hash1','business1');self.assertEqual(status,'DUPLICATE')
        ledger,status=receive(ledger,'d2','e1','hash1','business1');self.assertEqual(status,'DUPLICATE')
        self.assertEqual(len(ledger['tasks']),1)
    def test_content_collision_and_edit_quarantine(self):
        l,_=receive({},'d1','e1','hash1','k')
        self.assertEqual(receive(l,'d1','e1','hash2','k')[1],'QUARANTINED_DELIVERY_COLLISION')
        self.assertEqual(receive(l,'d2','e1','hash2','k')[1],'QUARANTINED_EVENT_EDIT')
    def test_no_blind_retry_after_disconnect(self):
        s,intent=publication_outcome({},'marker',{},body_digest='body-hash',target_ref='target');self.assertEqual(intent,'ONE_SEND_INTENT')
        s,intent=publication_outcome(s,'marker',{},body_digest='body-hash',target_ref='target',uncertain=True);self.assertEqual(intent,'RECONCILE_ONLY')
        s,intent=publication_outcome(s,'marker',{'marker':{'body_digest':'body-hash','target_ref':'target'}},body_digest='body-hash',target_ref='target');self.assertEqual((intent,s['publication']),('NO_SEND','CONFIRMED'))
    def test_ack_does_not_approve_or_close(self):
        t=review_signal(self.task,'ACKNOWLEDGED');self.assertEqual(t['states']['review'],'PENDING')
        with self.assertRaises(ValueError):review_signal(t,'CLOSE')
    def ready(self):
        t=review_signal(self.task,'RESULT_READY',sha=self.task['resource']['revision'])
        return review_signal(t,'PUBLICATION_CONFIRMED')
    def test_acceptance_wrong_owner_or_revision(self):
        t=self.ready()
        for owner,sha in [('urn:agentops:example-project:human:1','a'*40),('urn:agentops:example-project:human:2','b'*40)]:
            with self.assertRaises(ValueError):review_signal(t,'ACCEPT',actor_owner_id=owner,sha=sha,evidence=True,substantive=True)
    def test_full_synthetic_roundtrip(self):
        report=analyze_read_only(b'# Synthetic\nTODO: review\n');self.assertEqual(report['todo_count'],1)
        t=self.ready();t=review_signal(t,'ACCEPT',actor_owner_id='urn:agentops:example-project:human:2',sha='a'*40,evidence=True,substantive=True)
        t=review_signal(t,'CLOSE');self.assertEqual(t['states']['closure'],'CLOSED')
        with self.assertRaises(ValueError):review_signal(t,'ACKNOWLEDGED')
    def test_head_change_invalidates_acceptance(self):
        t=review_signal(self.ready(),'SHA_CHANGED')
        with self.assertRaises(ValueError):review_signal(t,'CLOSE')
        self.assertEqual(t['states']['review'],'STALE')
    def test_sql_constraints_local_only(self):
        with sqlite3.connect(':memory:') as db:
            db.executescript((ROOT/'agentops_reference/ledger.sql').read_text())
            db.execute('INSERT INTO events VALUES (?,?,?,?,?)',('p','e','h','source','r'))
            with self.assertRaises(sqlite3.IntegrityError):db.execute('INSERT INTO events VALUES (?,?,?,?,?)',('p','e','different','source','r'))
            db.execute('INSERT INTO tasks VALUES (?,?,?,?,?,?)',('p','t',1,'k',1,'{}'))
            with self.assertRaises(sqlite3.IntegrityError):db.execute('INSERT INTO tasks VALUES (?,?,?,?,?,?)',('p','other',1,'k',1,'{}'))

    def test_publication_wrong_body_or_target_quarantined(self):
        state,intent=publication_outcome({},'m',{'m':{'body_digest':'wrong','target_ref':'target'}},body_digest='h',target_ref='target')
        self.assertEqual(intent,'QUARANTINE_READBACK_MISMATCH')
        self.assertEqual(state['publication'],'FAILED')

    def test_message_loop_limits_and_unauthorized_actor(self):
        from agentops_reference.model import route_message
        args={'recipient_team':'team-a','configured_team':'team-a','policy_allows':True}
        for kind in ['ACKNOWLEDGED','CLOSED','BLOCKED','DECISION_REQUIRED']:
            self.assertEqual(route_message(kind,**args),'NO_EXECUTION')
        self.assertEqual(route_message('REVIEW_REQUIRED',**args,own_echo=True),'NO_EXECUTION')
        self.assertEqual(route_message('REVIEW_REQUIRED',**args,hop_count=4),'HOP_LIMIT')
        self.assertEqual(route_message('REVIEW_REQUIRED',**args,no_progress=2),'PREPARE_ONE_DECISION_REQUEST')
        self.assertEqual(route_message('REVIEW_REQUIRED',**args,no_progress=2,escalation_emitted=True),'STOP')
        args['policy_allows']=False
        self.assertEqual(route_message('REVIEW_REQUIRED',**args),'DENY')

    def test_read_retry_limits_and_retry_after(self):
        from agentops_reference.model import retry_read
        self.assertEqual(retry_read(503,1,20),{'retry':True,'delay_seconds':2})
        self.assertEqual(retry_read(503,2,20),{'retry':True,'delay_seconds':4})
        self.assertEqual(retry_read(503,3,20)['reason'],'CALL_LIMIT')
        for code in [401,403,404]:self.assertEqual(retry_read(code,1,20)['reason'],'ACCESS_BLOCKED')
        self.assertEqual(retry_read(429,1,20,retry_after=30)['reason'],'DEADLINE')
        self.assertEqual(retry_read(429,1,20,retry_after=10),{'retry':True,'delay_seconds':10})

    def test_demo_links_real_synthetic_bundle_digest_and_contracts(self):
        from agentops_reference.demo import run,serialized
        from agentops_reference.model import digest
        from agentops_reference.contracts import validate_semantics
        out=run();records=out['contract_records']
        for record in records.values():validate_semantics(record)
        self.assertEqual(out['evidence_digest'],digest(serialized(records['EvidenceBundle'])))
        self.assertEqual(records['ExecutionResult']['evidence_refs'][0]['digest'],out['evidence_digest'])
        self.assertEqual(records['HandoffMessage']['task_id'],records['Task']['id'])
        self.assertEqual(records['Task']['trigger_event_id'],records['Event']['id'])
        self.assertEqual(records['Task']['states']['closure'],'CLOSED')
        self.assertEqual(out['external_writes'],0)
