# SPDX-License-Identifier: MIT
"""Pure reducers: explicitly in-memory, no durable queue or external side effects."""
from copy import deepcopy
from hashlib import sha256
import json

def digest(data):
    return 'sha256:' + sha256(data).hexdigest()

def key(*parts):
    # Defined tuple encoding: UTF-8 compact JSON array of strings; no delimiter ambiguity.
    return digest(json.dumps(list(parts), ensure_ascii=False, separators=(',', ':')).encode())

def receive(ledger, delivery_id, event_id, payload_digest, business_key):
    state = deepcopy(ledger)
    deliveries = state.setdefault('deliveries', {})
    events = state.setdefault('events', {})
    tasks = state.setdefault('tasks', {})
    if delivery_id in deliveries and deliveries[delivery_id] != (event_id,payload_digest):
        return state, 'QUARANTINED_DELIVERY_COLLISION'
    if event_id in events and events[event_id] != payload_digest:
        return state, 'QUARANTINED_EVENT_EDIT'
    deliveries[delivery_id] = (event_id,payload_digest)
    events[event_id] = payload_digest
    if business_key in tasks:
        return state, 'DUPLICATE'
    tasks[business_key] = event_id
    return state, 'REGISTERED'

def analyze_read_only(blob):
    """Deterministic analysis of supplied synthetic bytes, never evaluates source code."""
    text = blob.decode('utf-8', errors='strict')
    return {'digest':digest(blob),'lines':len(text.splitlines()),'todo_count':text.count('TODO'),
            'claims_supported':['Supplied bytes inspected without code execution'],
            'claims_not_supported':['No application correctness, AI runtime or remote activation established']}

def publication_outcome(state, marker, observed_effects, *, body_digest, target_ref, uncertain=False):
    out = deepcopy(state)
    expected = {'body_digest':body_digest, 'target_ref':target_ref}
    if out and any(out.get(k) != v for k,v in expected.items()):
        raise ValueError('Publication scope changed')
    out.update(expected)
    if marker in observed_effects:
        if observed_effects[marker] != expected:
            out['publication'] = 'FAILED'
            return out, 'QUARANTINE_READBACK_MISMATCH'
        out['publication'] = 'CONFIRMED'
        return out, 'NO_SEND'
    if uncertain or out.get('publication') in {'SENDING','UNKNOWN','CONFIRMED'}:
        out['publication'] = 'UNKNOWN'
        return out, 'RECONCILE_ONLY'
    out['publication'] = 'SENDING'
    return out, 'ONE_SEND_INTENT'

def review_signal(task, signal, *, actor_owner_id=None, sha=None, evidence=False, substantive=False):
    out = deepcopy(task)
    states = out['states']
    if states['closure'] != 'OPEN':
        raise ValueError('Closed task is immutable; create linked successor')
    if signal == 'ACKNOWLEDGED':
        states['receipt'] = 'ACKNOWLEDGED'
    elif signal == 'RESULT_READY':
        if sha != task['resource']['revision']:
            states['execution'] = 'STALE'; states['review'] = 'STALE'
        else:
            states['execution'] = 'SUCCEEDED'; states['review'] = 'PENDING'
    elif signal == 'PUBLICATION_CONFIRMED':
        states['publication'] = 'CONFIRMED'
    elif signal == 'ACCEPT':
        if actor_owner_id != task['review_target']['owner_id'] or actor_owner_id == task['target']['owner_id']:
            raise ValueError('Acceptance requires distinct configured recipient owner')
        if sha != task['resource']['revision'] or not evidence or not substantive:
            raise ValueError('Acceptance lacks revision, evidence or substantive response')
        if states['execution'] != 'SUCCEEDED' or states['publication'] != 'CONFIRMED':
            raise ValueError('Result not ready for acceptance')
        states['review'] = 'ACCEPTED'; states['receipt'] = 'ACKNOWLEDGED'
    elif signal == 'CLOSE':
        if (states['execution'],states['review'],states['publication']) != ('SUCCEEDED','ACCEPTED','CONFIRMED'):
            raise ValueError('Closure criteria unmet')
        states['closure'] = 'CLOSED'
    elif signal == 'SHA_CHANGED':
        states['execution'] = 'STALE'; states['review'] = 'STALE'
    else:
        raise ValueError('Unknown signal')
    out['record_revision'] += 1
    return out

def route_message(message_type, *, recipient_team, configured_team, policy_allows, own_echo=False,
                  hop_count=0, max_hops=4, no_progress=0, escalation_emitted=False):
    """Pure scheduling decision. Trusted policy result is supplied by caller, not parsed content."""
    if not policy_allows or recipient_team != configured_team:
        return 'DENY'
    if own_echo or message_type in {'ACKNOWLEDGED','CLOSED','BLOCKED','DECISION_REQUIRED'}:
        return 'NO_EXECUTION'
    if message_type not in {'REVIEW_REQUIRED','READY_FOR_REVIEW','CHANGES_REQUESTED'}:
        return 'QUARANTINE'
    if hop_count >= max_hops:
        return 'HOP_LIMIT'
    if no_progress >= 2:
        return 'STOP' if escalation_emitted else 'PREPARE_ONE_DECISION_REQUEST'
    return 'SCHEDULABLE'

def retry_read(error_code, calls_used, remaining_seconds, retry_after=None, jitter=0):
    """Bounded read retries only; writes and executor attempts have independent grants."""
    if not 0 <= jitter <= 1 or calls_used < 1:
        raise ValueError('Invalid retry accounting')
    if error_code in {401,403,404}:
        return {'retry':False,'reason':'ACCESS_BLOCKED'}
    if calls_used >= 3:
        return {'retry':False,'reason':'CALL_LIMIT'}
    if error_code not in {429,500,502,503,504,'NETWORK'}:
        return {'retry':False,'reason':'NON_TRANSIENT'}
    delay = retry_after if retry_after is not None else (2 ** calls_used + jitter)
    if delay < 0 or delay >= remaining_seconds:
        return {'retry':False,'reason':'DEADLINE'}
    return {'retry':True,'delay_seconds':delay}
