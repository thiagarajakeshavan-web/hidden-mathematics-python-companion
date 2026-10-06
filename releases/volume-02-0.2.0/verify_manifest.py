#!/usr/bin/env python3
"""Verify SHA-256 file integrity, not publisher identity or security."""
import hashlib
import json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.sha256.json').read_text(encoding='utf-8'))
failures=[]
for name, expected in manifest['files'].items():
    path=root/name
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
        failures.append(name)
if failures:
    raise SystemExit('Integrity mismatch: '+', '.join(failures))
print(f"Verified {len(manifest['files'])} files. This is an integrity check, not a digital signature.")
