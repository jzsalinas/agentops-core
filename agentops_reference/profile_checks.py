# SPDX-License-Identifier: MIT
"""Selected offline profile experiments; not a runtime or a general profile validator.

Trusted facts/policy are supplied by the synthetic test harness. These functions
neither authenticate those facts nor reserve authority or perform external actions.
"""
import json
from .model import digest


def effect_decision(plan, facts, constraints):
    """Return one illustrative boundary decision; never execute or issue consent."""
    if plan['profile'] != 'agentops-effect-plan/0.1-experimental':
        return 'STOP_PROFILE'
    if facts['prior_effect'] in {'UNKNOWN', 'SENDING'}:
        return 'RECONCILE_ONLY'
    if facts['prior_effect'] == 'CONFIRMED':
        return 'NO_ACTION'
    if facts['prior_effect'] != 'NONE':
        return 'STOP_UNKNOWN_STATE'
    if not constraints['grant_checked'] or not constraints['tool_allows']:
        return 'STOP_AUTHORITY'
    step = plan['steps'][0]
    if (plan['task_id'] != facts['task_id'] or
            plan['task_revision'] != facts['task_revision'] or
            plan['resource'] != facts['resource'] or
            plan['policy_digest'] != facts['policy_digest'] or
            step['target_ref'] != facts['target_ref'] or
            step['body_digest'] != facts['body_digest']):
        return 'STOP_DRIFT'
    if (step['action'] not in constraints['actions'] or
            step['body_digest'] not in constraints['artifact_digests'] or
            constraints['remaining_effects'] < 1):
        return 'STOP_AUTHORITY'
    if facts['settled'] is not True:
        return 'WAIT_FOR_COMPLETION'
    if facts['dialogue'] == 'NEW_SCOPE':
        return 'DECISION_REQUIRED'
    if facts['dialogue'] == 'ROUTINE':
        if constraints['human_dialogue_policy'] != 'ALLOW_SAME_EFFECT':
            return 'DECISION_REQUIRED'
    elif facts['dialogue'] != 'NONE':
        return 'DECISION_REQUIRED'
    return 'READY_FOR_ONE_ACTION'


def criterion_outcomes(profile, observations, *, subject_revision):
    """Check selected fixture criteria against supplied bytes, not filenames/PASS.

    Observation provenance is simulated. Real authentication and domain procedures
    are deliberately outside this predicate. observations maps artifact keys to bytes.
    """
    if profile['profile'] != 'agentops-evidence-acceptance/0.1-experimental':
        raise ValueError('PROFILE_UNSUPPORTED')
    outcomes = {}
    for assertion in profile['assertions']:
        claim = assertion['claim_id']
        raw = observations.get(assertion['artifact_key'])
        if raw is None or digest(raw) != assertion['artifact_digest']:
            outcomes[claim] = 'UNSUPPORTED_INTEGRITY'
            continue
        try:
            observed = json.loads(raw)
            relevant = (
                assertion['subject_revision'] == subject_revision == observed['subject_revision']
                and assertion['subject_id'] == observed['subject_id']
                and assertion['required_class'] == observed['source_class']
                and assertion['procedure'] == observed['procedure']
                and assertion['producer'] == observed['producer']
                and observed['conditions'].get(assertion['condition']['field']) == assertion['condition']['equals']
            )
        except (ValueError, KeyError, TypeError, AttributeError):
            relevant = False
        outcomes[claim] = 'SUPPORTED' if relevant else 'UNSUPPORTED_CONDITION'
    return outcomes


def project_inventory(rows, *, selector, destination):
    """Project one synthetic row before emission; return no raw diagnostics.

    Fixed policies demonstrate value-shape checks as well as field selection.
    No logging, arbitrary free text, URL, nested data or caller-selected fields.
    """
    policies = {'MODEL_CONTEXT': ('resource_id', 'state'), 'PUBLIC_SUMMARY': ('state',)}
    if (not isinstance(destination, str) or not isinstance(selector, str) or
            destination not in policies or selector not in {'resource-allowed', 'resource-other'}):
        raise ValueError('PROJECTION_POLICY_DENIED')
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError('PROJECTION_SHAPE_DENIED')
    selected = [row for row in rows if row.get('resource_id') == selector]
    if len(selected) != 1:
        raise ValueError('PROJECTION_SELECTION_DENIED')
    row = selected[0]
    if not isinstance(row.get('state'), str) or row['state'] not in {'READY', 'PENDING'}:
        raise ValueError('PROJECTION_VALUE_DENIED')
    return {field: row[field] for field in policies[destination]}


def public_summary_allowed(summary):
    """Reject recognized URI/Markdown/HTML link forms in a bounded experiment.

    This is not a complete detector of every encoded or rendered link form.
    """
    from tools.audit_public import findings_for_text
    import re
    if findings_for_text('sample.txt', summary):
        return False
    return not re.search(
        r'(?:\b[A-Za-z][A-Za-z0-9+.-]*:\S|\]\s*\(|//\S|<(?:a|link|img)\b|\b(?:href|src)\s*=)',
        summary, re.I)
