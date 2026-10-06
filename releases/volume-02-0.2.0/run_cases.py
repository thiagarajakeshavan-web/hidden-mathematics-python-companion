#!/usr/bin/env python3
"""Run all fourteen offline labs or select one chapter. No network or credentials."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from volume2_companion.registry import CHAPTERS, CASES, execute, verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter", type=int, choices=CHAPTERS)
    parser.add_argument("--case", type=int, choices=(1, 2), help="select case number, optionally with --chapter")
    parser.add_argument("--verify", action="store_true", help="compare against recorded outputs")
    parser.add_argument("--output", type=Path, help="write JSON to this file instead of stdout")
    args = parser.parse_args()
    results = {}
    selected = [(c, n) for c, n in CASES if (args.chapter is None or c == args.chapter) and (args.case is None or n == args.case)]
    if not selected:
        parser.error("no matching chapter/case pair")
    for chapter, case_number in selected:
        result = execute(chapter, case_number)
        if args.verify:
            mismatches = verify(chapter, result, case_number)
            if mismatches:
                parser.exit(1, f"Chapter {chapter} differs at {mismatches}\n")
        results[f"V2C{chapter}-CASE{case_number:02d}"] = result
    text = json.dumps(results, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"Ran {len(results)} case(s); results: {args.output}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
