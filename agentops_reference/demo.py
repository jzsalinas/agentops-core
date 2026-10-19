# SPDX-License-Identifier: MIT
"""Offline contract-linked walkthrough. No network, processes or external side effects."""
import json
from pathlib import Path
from .contracts import validate_contract,validate_semantics,guard_execution
from .model import key,digest,receive,analyze_read_only,publication_outcome,review_signal
from .example_handoff import TrustedSource,normalize
ROOT=Path(__file__).resolve().parents[1]

def serialized(value):
    # Exact bytes chosen for this demo's evidence artifact; not a general JCS claim.
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')

def run():
    graph=json.loads((ROOT/'fixtures/contract-graph.json').read_text())
    for record in graph.values():validate_semantics(record)
    task=graph['Task'];msg=graph['HandoffMessage'];raw=(ROOT/'fixtures/synthetic-handoff.md').read_bytes()
    source=TrustedSource(task['project_id'],'example-project','https://example.invalid/comments/1','1',task['created_at'],task['created_at'],'urn:synthetic:snapshot:1','example-repository:request:1','example-principal-a','example-principal-a',msg['source'],msg['target'],msg['resource'])
    adapted=normalize(raw,source)['message']
    # Core classification for this synthetic request is explicit, not an import side effect.
    task.update(id=adapted['task_id'],correlation_id=adapted['correlation_id'],trigger_event_id=adapted['event_id'])
    task['idempotency_key']=key(task['project_id'],task['id'],'1',task['target']['team_id'],task['action'],task['resource']['revision'])
    for record in graph.values():
        if 'task_id' in record:record['task_id']=task['id']
    graph['Authorization']['scope']['task_id']=task['id'];graph['ApprovalRequest']['scope']['task_id']=task['id']
    event=graph['Event'];event.update(id=adapted['event_id'],correlation_id=task['id'],payload_digest=digest(raw),payload_ref=source.snapshot_ref)
    graph['HandoffMessage']=adapted
    business=task['idempotency_key']
    ledger,status=receive({},'synthetic-delivery-1',adapted['event_id'],digest(raw),business)
    ledger,duplicate=receive(ledger,'synthetic-delivery-2',adapted['event_id'],digest(raw),business)
    guard_execution(task,graph['Execution'],graph['TaskAssignment'],graph['Authorization'],'2025-01-01T12:01:00Z',fence=1)
    blob=b'# Synthetic repository\nTODO: review evidence\n'
    analysis=analyze_read_only(blob)
    bundle=graph['EvidenceBundle']
    bundle['artifacts']=[{'artifact_id':'urn:agentops:example-project:artifact:1','uri':'urn:synthetic:input:1','digest':digest(blob),'media_type':'text/plain','bytes':len(blob)}]
    bundle['claims_supported']=analysis['claims_supported'];bundle['claims_not_supported']=analysis['claims_not_supported']
    evidence_digest=digest(serialized(bundle))
    evidence_ref={'bundle_id':bundle['id'],'digest':evidence_digest}
    graph['ExecutionAttempt']['evidence_refs']=[evidence_ref];graph['ExecutionResult']['evidence_refs']=[evidence_ref]
    graph['ApprovalRequest']['prepared_bundle']=evidence_ref
    graph['Execution'].update(status='SUCCEEDED',attempt_ids=[graph['ExecutionAttempt']['id']])
    result=graph['ExecutionResult'];body_hash=digest(serialized(result));graph['ApprovalRequest']['scope']['artifact_digests']=[body_hash];target='https://example.invalid/synthetic/pull/1'
    pub,intent=publication_outcome({},'synthetic-effect-1',{},body_digest=body_hash,target_ref=target)
    pub,reconcile=publication_outcome(pub,'synthetic-effect-1',{},body_digest=body_hash,target_ref=target,uncertain=True)
    pub,readback=publication_outcome(pub,'synthetic-effect-1',{'synthetic-effect-1':{'body_digest':body_hash,'target_ref':target}},body_digest=body_hash,target_ref=target)
    task=review_signal(task,'RESULT_READY',sha=task['resource']['revision'])
    task=review_signal(task,'PUBLICATION_CONFIRMED')
    task=review_signal(task,'ACCEPT',actor_owner_id=task['review_target']['owner_id'],sha=task['resource']['revision'],evidence=True,substantive=True)
    task=review_signal(task,'CLOSE');graph['Task']=task
    for record in graph.values():validate_semantics(record)
    return {'scope':'VERIFIED only for local synthetic pure-function walkthrough; not remote pilot',
      'event_receipt':status,'duplicate':duplicate,'registered_tasks':len(ledger['tasks']),
      'analysis':analysis,'publication_simulation':[intent,reconcile,readback],
      'final_states':task['states'],'external_writes':0,'real_ai_runtime_started':False,
      'evidence_digest':evidence_digest,'evidence_encoding':'UTF-8 JSON sorted keys, ensure_ascii=False, separators=(comma,colon)',
      'contract_records':graph}

if __name__=='__main__':print(json.dumps(run(),indent=2))
