# SPDX-License-Identifier: MIT
"""Offline package/corpus checks, not a host discovery or live model evaluation."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'agentops-onboarding'


def frontmatter(path):
    text = path.read_text()
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise ValueError('Missing frontmatter')
    return yaml.safe_load(match[1])


def fixture_cases():
    return [json.loads(p.read_text()) for p in sorted((ROOT / 'fixtures/onboarding').glob('*.json'))]


def snapshot(root):
    return {p.relative_to(root).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mode)
            for p in root.rglob('*') if p.is_file()}


class OnboardingPackageTest(unittest.TestCase):
    def test_agent_skills_core_format(self):
        meta = frontmatter(SKILL / 'SKILL.md')
        self.assertEqual(set(meta), {'name', 'description', 'license'})
        self.assertEqual(meta['name'], SKILL.name)
        self.assertRegex(meta['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
        self.assertTrue(1 <= len(meta['name']) <= 64)
        self.assertIsInstance(meta['description'], str)
        self.assertTrue(1 <= len(meta['description']) <= 1024)
        self.assertEqual(meta['license'], 'MIT')

    def test_portable_resources_survive_relocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            moved = Path(tmp) / SKILL.name
            shutil.copytree(SKILL, moved)
            links = []
            for path in moved.rglob('*.md'):
                for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
                    self.assertNotIn(':', target, 'Portable skill must not need a remote resource')
                    dest = (path.parent / target.split('#')[0]).resolve()
                    self.assertTrue(dest.is_relative_to(moved))
                    self.assertTrue(dest.is_file())
                    links.append(dest)
            self.assertGreaterEqual(len(set(links)), 4)

    def test_package_is_instruction_only_and_has_no_hidden_payload(self):
        for path in SKILL.rglob('*'):
            self.assertFalse(path.is_symlink())
            self.assertFalse(path.name.startswith('.'))
            if path.is_file():
                self.assertEqual(path.suffix, '.md')
                self.assertNotIn('\x00', path.read_text())
                self.assertFalse(path.stat().st_mode & 0o111)

    def test_pending_snippet_cannot_supply_fabricated_pins(self):
        text = (SKILL / 'assets/AGENTS_SNIPPET.md').read_text()
        names = set(re.findall(r'\{\{([A-Z_]+)\}\}', text))
        self.assertEqual(names, {'ADOPTED_VERSION', 'SOURCE_COMMIT', 'ARTIFACT_DIGEST',
                                'EXISTING_ADOPTION_RECORD_REF', 'PROJECT_POLICY_REF',
                                'APPLICABLE_INSTRUCTIONS_REF'})
        self.assertNotRegex(text, r'\b[0-9a-f]{40,64}\b')

    def test_corpus_is_synthetic_complete_and_paths_are_bounded(self):
        cases = fixture_cases()
        ids = {c['id'] for c in cases}
        self.assertEqual(len(ids), len(cases))
        required = {'no-instructions', 'existing-agents', 'solo-small', 'multi-team',
                    'offline', 'declined', 'prerelease-only', 'incompatible-policy',
                    'unpublished-and-injection', 'self-asserted-digest'}
        self.assertEqual(ids, required)
        for case in cases:
            self.assertIs(case['synthetic'], True)
            self.assertEqual(case['format'], 'agentops-onboarding-scenario/1')
            self.assertTrue(case['request'])
            for name, text in case['files'].items():
                p = PurePosixPath(name)
                self.assertFalse(p.is_absolute())
                self.assertNotIn('..', p.parts)
                self.assertNotIn('\\', name)
                self.assertIsInstance(text, str)
                self.assertNotIn('\x00', text)
            self.assertNotIn('expected', case)

    def test_corpus_reads_preserve_content_with_execution_and_network_denied(self):
        # This checks the corpus harness only. Live assessment is recorded separately.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for case in fixture_cases():
                project = root / case['id']
                for name, text in case['files'].items():
                    path = project / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text)
            before = snapshot(root)
            with patch('socket.socket', side_effect=AssertionError('No network')), \
                 patch('subprocess.Popen', side_effect=AssertionError('No execution')):
                for path in root.rglob('*'):
                    if path.is_file():
                        path.read_text()
            self.assertEqual(snapshot(root), before)

    def test_license_is_preserved_at_distribution_root(self):
        # Standalone redistribution must include this notice, not just the license field.
        text = (ROOT / 'LICENSE').read_text()
        self.assertTrue(text.startswith('MIT License'))
        self.assertIn('Copyright', text)
        self.assertIn('permission notice', text)

    def test_synthetic_payload_matches_its_fixture_digests(self):
        # Arithmetic integrity of a fictional artifact, not authenticated publication.
        case = next(c for c in fixture_cases() if c['id'] == 'no-instructions')
        source = case['context']['source']
        raw = source['artifact_utf8'].encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), source['artifact_sha256'])
        payload = json.loads(raw)['files']
        self.assertEqual(set(payload), set(source['file_digests']))
        for name, text in payload.items():
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), source['file_digests'][name])
