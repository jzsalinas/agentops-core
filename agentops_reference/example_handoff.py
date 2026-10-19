# SPDX-License-Identifier: MIT
"""Additive EXAMPLE-HANDOFF reader for synthetic fixtures. Never publishes or grants authority."""
from copy import deepcopy
from dataclasses import dataclass
import re
import yaml
from yaml.tokens import AliasToken, AnchorToken, TagToken
from .model import digest, key
from .contracts import validate_contract

TYPES = {'REVIEW_REQUIRED','ACKNOWLEDGED','CHANGES_REQUESTED','READY_FOR_REVIEW','BLOCKED','DECISION_REQUIRED','CLOSED'}
class Quarantine(ValueError):
    pass

class UniqueSafeLoader(yaml.SafeLoader):
    yaml_implicit_resolvers = {k: [(tag,rx) for tag,rx in values if tag != 'tag:yaml.org,2002:timestamp'] for k,values in yaml.SafeLoader.yaml_implicit_resolvers.items()}

def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        name = loader.construct_object(key_node, deep=deep)
        if not isinstance(name,str) or name in result or name == '<<':
            raise Quarantine('Non-string, duplicate or merge key')
        result[name] = loader.construct_object(value_node, deep=deep)
    return result
UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

@dataclass(frozen=True)
class TrustedSource:
    # Must come from the transport verifier and registry, never from parsed YAML.
    project_id: str
    project_namespace: str
    source_url: str
    source_object_id: str
    source_updated_at: str
    observed_at: str
    snapshot_ref: str
    scope_id: str
    authenticated_subject: str
    expected_subject: str
    source_party: dict
    target_party: dict
    resource: dict

def parse_message(raw):
    if len(raw) > 65536:
        raise Quarantine('Body exceeds 64 KiB')
    try:
        text = raw.decode('utf-8')
        blocks = re.findall(r'^```(?:yaml|yml)[ \t]*\r?\n(.*?)^```[ \t]*\r?$', text, re.M | re.S)
        if len(blocks) != 1:
            raise Quarantine('Exactly one fenced YAML block required in this agentops_reference dialect')
        body = blocks[0]
        if any(isinstance(tok,(AliasToken,AnchorToken,TagToken)) for tok in yaml.scan(body)):
            raise Quarantine('Aliases, anchors and explicit tags disabled')
        value = yaml.load(body, Loader=UniqueSafeLoader)
        if not isinstance(value,dict) or value.get('protocol') != 'EXAMPLE-HANDOFF/1':
            raise Quarantine('Unknown protocol')
        required = {'request_id','message_id','revision','in_reply_to','type','task','from','to','context','summary','evidence','requested_action','resolution_condition'}
        if required - value.keys():
            raise Quarantine('Required example handoff field absent; retain snapshot for manual mapping')
        def depth(x):
            if isinstance(x,dict):return 1+max([depth(v) for v in x.values()] or [0])
            if isinstance(x,list):return 1+max([depth(v) for v in x] or [0])
            return 0
        if depth(value)>24:
            raise Quarantine('Nested value exceeds limit')
        if type(value['revision']) is not int or value['revision'] < 1 or value['type'] not in TYPES:
            raise Quarantine('Invalid revision or type')
        for field in ('request_id','message_id','task','summary','requested_action','resolution_condition'):
            if not isinstance(value[field],str) or not value[field] or len(value[field])>4000:
                raise Quarantine('Invalid scalar field: '+field)
        if value['in_reply_to'] is not None and not isinstance(value['in_reply_to'],str):
            raise Quarantine('Invalid causality reference')
        if any(not isinstance(value[f],dict) for f in ('from','to','context')) or not isinstance(value['evidence'],(dict,list)):
            raise Quarantine('Invalid declared metadata')
        return value
    except (yaml.YAMLError, UnicodeError, RecursionError, TypeError) as exc:
        raise Quarantine('Unsafe or unsupported YAML') from exc

def normalize(raw, source, causal_event_id=None, evidence_refs=()):
    value = parse_message(raw)
    if source.authenticated_subject != source.expected_subject:
        raise Quarantine('Transport actor not mapped by trusted registry')
    # Full task URI is preserved in immutable snapshot. Canonical task identity is
    # resolved by the transport adapter, not the untrusted `task` URL.
    task_id = 'urn:agentops:'+source.project_namespace+':task:'+key(source.scope_id,value['request_id']).split(':')[1]
    event_id = 'urn:agentops:'+source.project_namespace+':event:'+key(source.scope_id,source.authenticated_subject,value['message_id']).split(':')[1]
    message_id = event_id.replace(':event:',':message:')
    losses = ['Declared evidence not independently resolved; no execution or authority inferred']
    if value['in_reply_to'] is not None and causal_event_id is None:
        losses.append('Unresolved causality reference retained in legacy.in_reply_to')
    normalized = {'schema_version':'AGENTOPS/1','kind':'HandoffMessage','id':message_id,'record_revision':1,
      'project_id':source.project_id,'created_at':source.observed_at,'task_id':task_id,'task_revision':value['revision'],
      'event_id':event_id,'correlation_id':task_id,'causation_id':causal_event_id,'type':value['type'],
      'source':deepcopy(source.source_party),'target':deepcopy(source.target_party),'resource':deepcopy(source.resource),
      'summary':value['summary'],'requested_action':value['requested_action'],'resolution_condition':value['resolution_condition'],
      'evidence_refs':list(evidence_refs),
      'legacy':{'protocol':'EXAMPLE-HANDOFF/1','request_id':value['request_id'],'message_id':value['message_id'],
        'revision':value['revision'],'in_reply_to':value['in_reply_to'],'declared_task':value['task'],'source_url':source.source_url,
        'source_object_id':source.source_object_id,'source_updated_at':source.source_updated_at,'observed_at':source.observed_at,
        'body_digest':digest(raw),'snapshot_ref':source.snapshot_ref,'parser_version':'example-handoff-fixture/0.1',
        'losses':losses,'declared_from':value['from'],'declared_to':value['to'],'declared_context':value['context'],'declared_evidence':value['evidence']}}
    validate_contract(normalized)
    # Original bytes returned unchanged; caller decides secure storage and retention.
    return {'message':normalized,'snapshot_bytes':raw,'schedule_execution':False,'authority_granted':False}
