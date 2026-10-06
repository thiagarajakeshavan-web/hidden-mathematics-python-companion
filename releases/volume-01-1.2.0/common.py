"""Shared, deliberately small output helpers. No network or private data access."""
from pathlib import Path
import json
import os
# Process-local cap avoids unreliable physical-core discovery in small containers.
# It does not alter the reader's shell or operating-system settings.
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")
import numpy as np

ROOT = Path(__file__).resolve().parent
RELEASE = "1.1.0-author-review"

def plain(value):
    if isinstance(value, np.ndarray):
        return plain(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value

def emit(chapter, result):
    result = plain(result)
    destination = ROOT / chapter / "results.json"
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return result
