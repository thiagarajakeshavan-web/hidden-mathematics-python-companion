"""Verify byte preservation of inventoried original companion content."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parent


def verify():
    record = json.loads((ROOT / "BASELINE_PRESERVATION.json").read_text(encoding="utf-8"))
    problems = []
    for entry in record["preserved_files"]:
        relative = PurePosixPath(entry["path"])
        if relative.is_absolute() or ".." in relative.parts:
            problems.append(f"Unsafe path: {relative}")
            continue
        path = ROOT.joinpath(*relative.parts)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            problems.append(f"Changed or missing: {relative}")
    if problems:
        print("\n".join(problems))
        return False
    print(f"Verified {len(record['preserved_files'])} original files preserved byte-for-byte.")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
