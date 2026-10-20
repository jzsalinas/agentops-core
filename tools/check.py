# SPDX-License-Identifier: MIT
"""Run local checks without modifying the source tree or making remote requests."""
import io
import importlib.metadata
import json
from pathlib import Path
import re
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from agentops_reference.contracts import validate_contract
from agentops_reference.demo import run


def check():
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
    result = unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    if not result.wasSuccessful():
        return {'status':'FAIL','tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'details':'Inspect failures locally; raw tracebacks are not release artifacts.'}
    validate_contract(json.loads((ROOT/'templates/project/project.json').read_text()))
    run()
    links = 0
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if ':' in target or target.startswith('#'):
                continue
            dest = (path.parent / target.split('#')[0]).resolve()
            if not dest.is_relative_to(ROOT) or not dest.exists():
                raise ValueError('Internal link invalid')
            links += 1
    index = json.loads((ROOT/'schemas/1/examples/index.json').read_text())
    packages = ['jsonschema','referencing','PyYAML','attrs','jsonschema-specifications','rpds-py']
    return {'status':'PASS','scope':'Local schemas, selected guards, pure synthetic reference functions, format/privacy checks, in-memory SQL constraints and onboarding package/corpus checks only',
      'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
      'schema_files':len(list((ROOT/'schemas/1').glob('*.schema.json'))),'positive_examples':sum(x['valid'] for x in index),'negative_examples':sum(not x['valid'] for x in index),
      'internal_links_checked':links,'python_version':'.'.join(map(str,sys.version_info[:3])),
      'dependencies':{n:importlib.metadata.version(n) for n in packages},
      'remote_requests':0,'model_invocations':0,'external_effects':0,'workflows_created':0,
      'not_verified':['Operational authority issuer','Real provider execution','Remote delivery or publication','Durable worker or multiprocess crash recovery','Production operations','External protocol compatibility','Host skill installation or discovery','Live model evaluation (reported separately)','Consumer adoption or activation','Cryptographic release verification for onboarding']}


if __name__ == '__main__':
    try:
        report = check()
    except (ValueError, OSError, KeyError, ImportError):
        report = {'status':'FAIL','details':'Local validation could not complete; inspect the environment privately.'}
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['status']=='PASS' else 1)
