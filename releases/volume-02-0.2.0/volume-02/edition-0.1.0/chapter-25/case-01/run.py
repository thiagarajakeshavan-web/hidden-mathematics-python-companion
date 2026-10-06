#!/usr/bin/env python3
"""Run V2C25-CASE01 from any current working directory."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from volume2_companion.registry import execute, verify
result = execute(25)
errors = verify(25, result)
if errors:
    raise SystemExit(f"Result mismatch: {errors}")
print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
