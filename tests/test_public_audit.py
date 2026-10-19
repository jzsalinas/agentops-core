# SPDX-License-Identifier: MIT
import io
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile, ZipInfo
from tools.audit_public import findings_for_text, inspect_files, audit_directory, audit_archive

class PublicAuditTest(unittest.TestCase):
    def test_host_path_and_secret_detection(self):
        path = '/' + 'ho' + 'me' + '/' + 'example-user/file'
        token = 'gh' + 'p_' + 'A' * 24
        categories = {f['category'] for f in findings_for_text('sample.txt', path + '\n' + token)}
        self.assertEqual(categories, {'host-path', 'credential'})

    def test_reserved_hosts_and_unapproved_host(self):
        self.assertEqual(findings_for_text('sample.txt', 'https://example.org/reference'), [])
        url = 'https://' + 'unapproved.' + 'test-host'
        self.assertEqual(findings_for_text('sample.txt', url)[0]['category'], 'unapproved-host')

    def test_copyright_exception_is_exact_and_scoped(self):
        notice = 'Copyright (c) 2025 ' + 'example-maintainer'
        policy = {'approved_copyright_notice': notice, 'forbidden_patterns': [{'category':'private-marker','pattern':'example-maintainer'}]}
        self.assertEqual(findings_for_text('LICENSE',notice,policy), [])
        self.assertTrue(findings_for_text('README.md',notice,policy))
        self.assertTrue(findings_for_text('LICENSE',notice+' extra',policy))

    def test_unicode_and_json_escaped_marker(self):
        policy = {'forbidden_patterns':[{'category':'private-marker','pattern':'example-private-marker'}]}
        marker = 'example-private-marker'
        text = json.dumps({'value':marker}).replace('example', '\\u0065xample')
        findings = inspect_files({'sample.json':text.encode()},policy,verify_manifest=False)
        self.assertTrue(any(f.get('location')=='decoded-string' for f in findings))
        split = 'example-pri' + chr(0x200b) + 'vate-marker'
        self.assertTrue(findings_for_text('sample.txt',split,policy))

    def test_hidden_file_and_binary_detection(self):
        findings = inspect_files({'.env':b'SYNTHETIC=1','sample.txt':b'\x00'},verify_manifest=False)
        self.assertEqual({f['category'] for f in findings}, {'unapproved-hidden-file','binary-or-nonutf8'})

    def test_symlink_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'sample.txt').write_text('synthetic');(root/'link').symlink_to(root/'sample.txt')
            result=audit_directory(root,verify_manifest=False)
            self.assertTrue(any(f['category']=='symlink' for f in result['findings']))

    def test_manifest_failure_is_not_silently_accepted(self):
        result=inspect_files({'README.md':b'synthetic'})
        self.assertTrue(any(f['category']=='invalid-manifest' for f in result))

    def test_archive_metadata_is_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'sample.zip'
            with ZipFile(path,'w') as archive:
                info=ZipInfo('agentops-core/README.md',date_time=(2025,1,1,0,0,0));info.comment=b'synthetic';archive.writestr(info,b'synthetic')
            result=audit_archive(path)
            self.assertTrue(any(f['category']=='archive-metadata' for f in result['findings']))
