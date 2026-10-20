# SPDX-License-Identifier: MIT
"""Bounded public-export audit. Private denylist data is never copied into output."""
import argparse
import ast
import html
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import unicodedata
from urllib.parse import urlsplit
from zipfile import ZipFile

OFFICIAL_HOSTS = {
    'json-schema.org', 'pypi.org', 'spdx.org', 'opensource.org', 'docs.github.com',
    # Exact primary documentation hosts used by the optional onboarding guide.
    'learn.chatgpt.com', 'agentskills.io', 'code.claude.com',
}
METADATA_FILES = {'PUBLIC_FILES.json', 'MANIFEST.sha256'}
HIDDEN_ALLOWED = {'.gitignore', '.gitattributes'}


def folded(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text).casefold() if not unicodedata.combining(c) and unicodedata.category(c) != 'Cf')


def safe_name(name):
    p = PurePosixPath(name)
    return bool(name and not p.is_absolute() and '..' not in p.parts and '\\' not in name and '\x00' not in name)


def findings_for_text(name, text, private_policy=None):
    policy = private_policy or {}
    findings = []
    generic = [
        ('host-path', r'/(?:home|Users|root|tmp|var|etc|usr|srv|opt)/(?:[^\s"\x27<>]+)'),
        ('host-path', r'(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s"\x27<>]+'),
        ('email', r'(?<![\w.-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
        ('phone', r'(?<![A-Za-z0-9])\+[1-9][0-9 .()-]{8,}[0-9]'),
        ('credential', r'\bgh[pousr]_[A-Za-z0-9]{20,}'),
        ('credential', r'\bsk-[A-Za-z0-9_-]{20,}'),
        ('credential', r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
        ('private-key', r'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----'),
        ('cloud-resource', r'\barn:(?:aws|aws-cn|aws-us-gov):'),
    ]
    for lineno, line in enumerate(text.splitlines(), 1):
        for category, pattern in generic:
            if re.search(pattern, line):
                findings.append({'file': name, 'line': lineno, 'category': category})
        approved_notice = name == 'LICENSE' and line == policy.get('approved_copyright_notice')
        if not approved_notice:
            for rule in policy.get('forbidden_patterns', []):
                if re.search(rule['pattern'], folded(line), re.I):
                    findings.append({'file': name, 'line': lineno, 'category': rule['category']})
        for url in re.findall(r'https?://[^\s<>"\x27)]+', line):
            try:
                host = (urlsplit(url.rstrip('.,;')).hostname or '').lower()
                example = host in {'example.com','example.net','example.org','localhost'} or host.endswith(('.example.com','.example.net','.example.org','.invalid','.test','.localhost'))
                if not host and name.startswith('tests/'):
                    continue  # Malformed URI rejection cases are synthetic test input.
                if not example and host not in OFFICIAL_HOSTS:
                    findings.append({'file': name, 'line': lineno, 'category': 'unapproved-host'})
            except ValueError:
                findings.append({'file': name, 'line': lineno, 'category': 'invalid-url'})
    return findings


def inspect_files(files, private_policy=None, verify_manifest=True):
    findings = []
    policy = private_policy or {}
    canonical = set()
    for name, raw in sorted(files.items()):
        if not safe_name(name):
            findings.append({'file': '<unsafe-name>', 'category': 'unsafe-path'})
            continue
        normalized = folded(name)
        if normalized in canonical:
            findings.append({'file': name, 'category': 'ambiguous-name'})
        canonical.add(normalized)
        if any(part.startswith('.') for part in PurePosixPath(name).parts) and name not in HIDDEN_ALLOWED:
            findings.append({'file': name, 'category': 'unapproved-hidden-file'})
        if PurePosixPath(name).suffix not in {'.md','.py','.json','.sql','.txt','.sha256',''} and name not in HIDDEN_ALLOWED:
            findings.append({'file': name, 'category': 'unapproved-file-type'})
        findings.extend(findings_for_text('<path>', name, policy))
        try:
            text = raw.decode('utf-8')
            if '\x00' in text:
                raise UnicodeError()
        except (UnicodeError, UnicodeDecodeError):
            findings.append({'file': name, 'category': 'binary-or-nonutf8'})
            continue
        findings.extend(findings_for_text(name, text, policy))
        decoded = html.unescape(text)
        if decoded != text:
            findings.extend(findings_for_text(name, decoded, policy))
        semantic_strings = []
        def collect(value):
            if isinstance(value, str):
                semantic_strings.append(value)
            elif isinstance(value, dict):
                for key, child in value.items():
                    collect(key); collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)
        try:
            if name.endswith('.json'):
                collect(json.loads(text))
            elif name.endswith('.py'):
                for node in ast.walk(ast.parse(text)):
                    if isinstance(node, ast.Constant) and isinstance(node.value, str):
                        semantic_strings.append(node.value)
        except (ValueError, SyntaxError):
            findings.append({'file': name, 'category': 'unparseable-structured-text'})
        for value in semantic_strings:
            for finding in findings_for_text(name, value, policy):
                finding['location'] = 'decoded-string'
                findings.append(finding)
    notice = policy.get('approved_copyright_notice')
    if notice:
        occurrences = sum(raw.decode('utf-8',errors='replace').count(notice) for raw in files.values())
        if occurrences != 1 or notice not in files.get('LICENSE', b'').decode('utf-8',errors='replace').splitlines():
            findings.append({'file': 'LICENSE', 'category': 'copyright-exception-mismatch'})
    if verify_manifest:
        try:
            manifest = json.loads(files['PUBLIC_FILES.json'])
            entries = manifest['files']
            expected = {entry['path'] for entry in entries} | METADATA_FILES
            if len(entries) != len({entry['path'] for entry in entries}) or set(files) != expected:
                findings.append({'file': 'PUBLIC_FILES.json', 'category': 'allowlist-mismatch'})
            for entry in entries:
                raw = files.get(entry['path'])
                if raw is None or len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
                    findings.append({'file': entry['path'], 'category': 'digest-mismatch'})
            checksums = {}
            for line in files['MANIFEST.sha256'].decode().splitlines():
                h, name = line.split('  ', 1)
                if name in checksums:
                    raise ValueError('Duplicate checksum')
                checksums[name] = h
            if set(checksums) != set(files) - {'MANIFEST.sha256'}:
                findings.append({'file': 'MANIFEST.sha256', 'category': 'checksum-inventory-mismatch'})
            for name, h in checksums.items():
                if name not in files or hashlib.sha256(files[name]).hexdigest() != h:
                    findings.append({'file': name, 'category': 'checksum-mismatch'})
        except (KeyError, ValueError, TypeError):
            findings.append({'file': 'PUBLIC_FILES.json', 'category': 'invalid-manifest'})
    return findings


def audit_directory(root, private_policy=None, verify_manifest=True):
    files = {}
    findings = []
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            findings.append({'file': name, 'category': 'symlink'})
        elif path.is_file():
            files[name] = path.read_bytes()
        elif path.is_dir() and path.name.startswith('.') and name not in HIDDEN_ALLOWED:
            findings.append({'file': name, 'category': 'unapproved-hidden-directory'})
    findings.extend(inspect_files(files, private_policy, verify_manifest))
    return {'status': 'PASS' if not findings else 'FAIL', 'files_checked': len(files), 'private_policy_applied': bool(private_policy), 'findings': findings}


def audit_archive(path, private_policy=None):
    files = {}
    findings = []
    with ZipFile(path) as archive:
        if archive.comment:
            findings.append({'file': '<archive>', 'category': 'archive-comment'})
        infos = archive.infolist()
        if len(infos) > 512 or sum(i.file_size for i in infos) > 16 * 1024 * 1024:
            raise ValueError('Archive limit')
        for info in infos:
            if not safe_name(info.filename) or not info.filename.startswith('agentops-core/'):
                raise ValueError('Unsafe archive member')
            name = info.filename.removeprefix('agentops-core/')
            if name in files or info.flag_bits & 1 or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError('Invalid archive member')
            if info.comment or info.extra or info.date_time != (1980,1,1,0,0,0):
                findings.append({'file': name, 'category': 'archive-metadata'})
            if info.file_size / max(info.compress_size,1) > 1000:
                raise ValueError('Archive expansion limit')
            files[name] = archive.read(info)
        if archive.testzip() is not None:
            raise ValueError('Archive CRC')
    findings.extend(inspect_files(files, private_policy))
    return {'status': 'PASS' if not findings else 'FAIL', 'files_checked': len(files), 'private_policy_applied': bool(private_policy), 'findings': findings}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private-policy', type=Path, help='Maintainer-controlled policy outside the public export; never copied into output')
    parser.add_argument('--archive', type=Path, help='Inspect a prepared archive, including metadata')
    args = parser.parse_args()
    try:
        policy = json.loads(args.private_policy.read_text()) if args.private_policy else None
        report = audit_archive(args.archive,policy) if args.archive else audit_directory(Path(__file__).resolve().parents[1],policy)
        print(json.dumps(report,indent=2))
        raise SystemExit(0 if report['status']=='PASS' else 1)
    except (OSError, ValueError, TypeError):
        print(json.dumps({'status':'FAIL','category':'audit-input-or-archive-error'}))
        raise SystemExit(1)
