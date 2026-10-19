# SPDX-License-Identifier: MIT
"""Offline structural and selected semantic checks. No network or authority issuance."""
import json
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

SCHEMAS = Path(__file__).resolve().parents[1] / 'schemas' / '1'

def stamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))

# Formats are enforced explicitly; optional format plugins are not required.
FORMAT_CHECKER = FormatChecker(formats=[])

@FORMAT_CHECKER.checks('date-time')
def timestamp_format(value):
    if not isinstance(value, str):
        return True
    import re
    if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])', value):
        return False
    try:
        return stamp(value).tzinfo is not None
    except ValueError:
        return False

@FORMAT_CHECKER.checks('uri')
def absolute_uri_format(value):
    if not isinstance(value, str):
        return True
    import re
    from urllib.parse import urlsplit
    # A conservative ASCII absolute-URI profile; encoded non-ASCII is allowed.
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9+.-]*:[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+", value):
        return False
    if re.search(r'%(?![0-9A-Fa-f]{2})', value):
        return False
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() in {'http', 'https'} and not parsed.hostname:
            return False
        if parsed.netloc:
            parsed.port
        if any(c in parsed.path + parsed.query + parsed.fragment for c in '[]'):
            return False
        return bool(parsed.scheme and (parsed.netloc or parsed.path))
    except ValueError:
        return False


@lru_cache(maxsize=1)
def registry():
    pairs = []
    for path in SCHEMAS.glob('*.schema.json'):
        schema = json.loads(path.read_text())
        def formats(value):
            if isinstance(value, dict):
                if 'format' in value and value['format'] not in FORMAT_CHECKER.checkers:
                    raise ValueError('Unsupported format')
                for child in value.values():
                    formats(child)
            elif isinstance(value, list):
                for child in value:
                    formats(child)
        formats(schema)
        Draft202012Validator.check_schema(schema)
        pairs.append((schema['$id'], Resource.from_contents(schema)))
    # Every reference is registered locally; no retrieval fallback is supplied.
    return Registry().with_resources(pairs)

def validate_contract(value, name=None):
    name = name or value.get('kind', '')
    if name not in {p.name.removesuffix('.schema.json') for p in SCHEMAS.glob('*.schema.json')} - {'common'}:
        raise ValueError('Unknown contract kind')
    schema = json.loads((SCHEMAS / (name + '.schema.json')).read_text())
    Draft202012Validator(schema, registry=registry(), format_checker=FORMAT_CHECKER).validate(value)
    return value

def validate_semantics(value):
    validate_contract(value)
    kind = value['kind']
    if 'resource' in value and value['resource']['revision_status'] == 'UNKNOWN':
        if kind in {'Execution','ExecutionResult','TaskAssignment'}:
            raise ValueError('Execution requires pinned revision')
    if kind == 'Task':
        if value['states']['closure'] == 'CLOSED' and (value['states']['execution'],value['states']['review'],value['states']['publication']) != ('SUCCEEDED','ACCEPTED','CONFIRMED'):
            raise ValueError('Invalid closed task')
        if value['states']['review'] == 'ACCEPTED' and value['resource']['revision_status'] != 'PINNED':
            raise ValueError('Cannot accept unknown revision')
        if value['review_target']['owner_id'] == value['target']['owner_id']:
            raise ValueError('Pilot requires independent review owner')
        if value['correlation_id'] != value['id']:
            raise ValueError('Task correlation must be its stable task id')
        if stamp(value['deadline_at']) <= stamp(value['created_at']):
            raise ValueError('Non-positive deadline')
    if kind == 'Authorization':
        if stamp(value['valid_from']) >= stamp(value['expires_at']):
            raise ValueError('Invalid authorization window')
        if value['used_count'] > value['max_uses']:
            raise ValueError('Authorization use overflow')
        if value['status'] == 'CONSUMED' and value['used_count'] != value['max_uses']:
            raise ValueError('Inconsistent consumption')
    if kind == 'ExecutionAttempt':
        if value['ended_at'] and stamp(value['ended_at']) < stamp(value['started_at']):
            raise ValueError('Negative attempt duration')
        if value['status'] == 'RUNNING' and value['ended_at'] is not None:
            raise ValueError('Running attempt has ended')
        if value['status'] not in {'RUNNING','UNKNOWN'} and not value['ended_at']:
            raise ValueError('Terminal attempt needs end time')
    if kind == 'ApprovalRequest' and value['status'] == 'APPROVED' and value['decision_ref'] is None:
        raise ValueError('Approval needs external decision evidence')
    if kind in {'EvidenceBundle','ExecutionResult'}:
        if set(value['claims_supported']) & set(value['claims_not_supported']):
            raise ValueError('Contradictory claims')
    return value

def guard_execution(task, execution, assignment, authorization, now, attempt_number=1, fence=None):
    """Representative preflight, called with trusted store records, never payload grants."""
    for value in (task, execution, assignment, authorization):
        validate_semantics(value)
    if task['states']['closure'] != 'OPEN' or task['states']['execution'] not in {'QUEUED','CLAIMED'} or execution['status'] not in {'QUEUED','CLAIMED'} or execution['cancel_requested']:
        raise ValueError('Task no longer executable')
    if not all(v['project_id'] == task['project_id'] for v in (execution,assignment,authorization)):
        raise ValueError('Cross-project delegation')
    if any(v['task_id'] != task['id'] or v['task_revision'] != task['task_revision'] for v in (execution,assignment,authorization['scope'])):
        raise ValueError('Task/revision mismatch')
    if not (execution['resource'] == authorization['scope']['resource'] == task['resource']):
        raise ValueError('Resource drift')
    if task['resource']['revision_status'] != 'PINNED':
        raise ValueError('Unknown revision')
    if assignment['execution_id'] != execution['id'] or execution['assignment_id'] != assignment['id']:
        raise ValueError('Assignment linkage')
    if assignment['executor_id'] != execution['executor_id']:
        raise ValueError('Executor mismatch')
    if task['resource']['resource_id'] not in assignment['exclusive_resource_ids']:
        raise ValueError('Resource not leased')
    if assignment['agent_id'] != authorization['grantee_agent_id'] or assignment['agent_id'] != task['target']['agent_id']:
        raise ValueError('Wrong grantee')
    if execution['authorization_id'] != authorization['id'] or assignment['authorization_id'] != authorization['id']:
        raise ValueError('Wrong authorization reference')
    if not (execution['policy_digest'] == task['policy_digest'] == authorization['policy_digest']):
        raise ValueError('Policy drift')
    if task['action'] not in authorization['scope']['actions']:
        raise ValueError('Action not granted')
    instant = stamp(now)
    if not (stamp(authorization['valid_from']) <= instant < stamp(authorization['expires_at'])):
        raise ValueError('Authorization not active')
    if instant >= stamp(task['deadline_at']) or instant >= stamp(assignment['lease_expires_at']):
        raise ValueError('Deadline or lease expired')
    if authorization['status'] != 'GRANTED' or authorization['used_count'] >= authorization['max_uses']:
        raise ValueError('Authorization unavailable')
    if not 1 <= attempt_number <= min(task['budget']['max_attempts'], execution['budget']['max_attempts'], authorization['max_uses']):
        raise ValueError('Attempt limit')
    if fence is not None and fence != assignment['fencing_token']:
        raise ValueError('Stale fencing token')
    for key in ('max_attempts','wall_seconds','max_tokens','max_cost_minor','max_external_effects','max_hops','max_no_progress_exchanges'):
        if execution['budget'][key] > task['budget'][key]:
            raise ValueError('Child budget escalation')
    if execution['budget']['currency'] != task['budget']['currency']:
        raise ValueError('Currency mismatch')
    return True
