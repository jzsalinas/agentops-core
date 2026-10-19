# SPDX-License-Identifier: MIT
import copy
import json
from pathlib import Path
import unittest
from jsonschema import ValidationError
from agentops_reference.contracts import validate_contract, absolute_uri_format

ROOT = Path(__file__).resolve().parents[1]

class FormatTest(unittest.TestCase):
    def test_calendar_and_timezone_validation(self):
        task = json.loads((ROOT / 'schemas/1/examples/valid/Task.json').read_text())
        for date in ['2025-13-01T12:00:00Z', '2025-02-30T12:00:00Z', '2025-01-01T12:00:00', '2025-01-01T12:00:00+25:00']:
            with self.subTest(date=date):
                value = copy.deepcopy(task)
                value['created_at'] = date
                with self.assertRaises(ValidationError):
                    validate_contract(value)

    def test_malformed_absolute_uri_rejected(self):
        for uri in ['relative/path', 'https://', 'https:///missing-host', 'https://example.invalid/%GG', 'https://example.invalid:invalid', 'https://example.invalid/white space']:
            with self.subTest(uri=uri):
                self.assertFalse(absolute_uri_format(uri))

    def test_reserved_examples_and_urns(self):
        for uri in ['https://example.org/reference', 'https://example.invalid/%C3%A9', 'urn:agentops:example-project:task:1']:
            self.assertTrue(absolute_uri_format(uri))

    def test_unknown_format_fails_closed(self):
        import tempfile
        from unittest.mock import patch
        import agentops_reference.contracts as contracts
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp)
            schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'https://schemas.example.org/agentops/unsupported','type':'string','format':'unsupported-example-format'}
            (directory/'unsupported.schema.json').write_text(json.dumps(schema))
            contracts.registry.cache_clear()
            try:
                with patch.object(contracts,'SCHEMAS',directory):
                    with self.assertRaises(ValueError):
                        contracts.registry()
            finally:
                contracts.registry.cache_clear()
