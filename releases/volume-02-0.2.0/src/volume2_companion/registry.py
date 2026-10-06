"""Versioned case discovery and tolerance-aware reproducibility checks."""
import importlib
import json
import math
from pathlib import Path
from .numerics import json_ready

ROOT = Path(__file__).resolve().parents[2]
EDITION = "edition-0.1.0"
CHAPTERS = tuple(range(15, 27))
CASES = tuple((c, 1) for c in CHAPTERS) + ((15, 2), (16, 2))
NEW_MODULES = {15: "chapter15_optimizers", 16: "chapter16_normalization"}


def case_directory(chapter, case_number=1):
    if chapter not in CHAPTERS:
        raise ValueError("supported chapters are 15 through 26")
    if (chapter, case_number) not in CASES:
        raise ValueError("unsupported chapter/case pair")
    edition = EDITION if case_number == 1 else "edition-0.2.0"
    return ROOT / "volume-02" / edition / f"chapter-{chapter}" / f"case-{case_number:02d}"


def load_inputs(chapter, case_number=1):
    return json.loads((case_directory(chapter, case_number)/"fixture.json").read_text(encoding="utf-8"))


def execute(chapter, case_number=1):
    case = load_inputs(chapter, case_number)
    module = f"chapter{chapter}" if case_number == 1 else NEW_MODULES[chapter]
    return json_ready(importlib.import_module(f"volume2_companion.{module}").run(case["inputs"]))


def differences(actual, expected, path="result", atol=1e-9, rtol=1e-9):
    """Return discrepancies; booleans are not interchangeable with numeric 0/1."""
    if isinstance(expected, bool) or expected is None or isinstance(expected, str):
        return [] if type(actual) is type(expected) and actual == expected else [path]
    if isinstance(expected, (int, float)):
        return [] if not isinstance(actual, bool) and isinstance(actual, (int, float)) and math.isclose(actual, expected, abs_tol=atol, rel_tol=rtol) else [path]
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            return [path]
        return [d for j, (a, e) in enumerate(zip(actual, expected)) for d in differences(a, e, f"{path}[{j}]", atol, rtol)]
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(actual) != set(expected):
            return [path]
        return [d for k in expected for d in differences(actual[k], expected[k], f"{path}.{k}", atol, rtol)]
    raise TypeError(f"unsupported expected result type at {path}")


def verify(chapter, actual, case_number=1):
    expected = json.loads((case_directory(chapter, case_number)/"expected.json").read_text(encoding="utf-8"))
    return differences(actual, expected)
