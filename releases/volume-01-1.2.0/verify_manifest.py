"""Verify the included file inventory without downloading or changing files."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parent

def verify():
    manifest=json.loads((ROOT/"MANIFEST.json").read_text(encoding="utf-8"))
    problems=[]
    for entry in manifest["files"]:
        relative=PurePosixPath(entry["path"])
        if relative.is_absolute() or ".." in relative.parts:
            problems.append(f"Unsafe inventory path: {relative}");continue
        path=ROOT.joinpath(*relative.parts)
        if not path.is_file(): problems.append(f"Missing: {relative}");continue
        data=path.read_bytes()
        if len(data)!=entry["bytes"] or hashlib.sha256(data).hexdigest()!=entry["sha256"]:
            problems.append(f"Changed: {relative}")
    if problems:
        print("\n".join(problems));return False
    print(f"Verified {len(manifest['files'])} files for {manifest['release']}.")
    return True

if __name__ == "__main__": sys.exit(0 if verify() else 1)
