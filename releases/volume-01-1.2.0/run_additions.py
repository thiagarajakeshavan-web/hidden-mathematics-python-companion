"""Refresh only the new 1.2.0 teaching outputs, preserving existing lab outputs."""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parent


def main():
    pairs = [
        ("shopsmart_scenarios/grocery30.py", "shopsmart_scenarios/grocery30_results.json"),
        ("shopsmart_scenarios/timing30.py", "shopsmart_scenarios/timing30_results.json"),
        ("shopsmart_scenarios/dinner5.py", "shopsmart_scenarios/dinner5_results.json"),
        ("V1C04/CASE02/map_mle.py", "V1C04/CASE02/results.json"),
        ("V1C07/CASE02/no_free_lunch.py", "V1C07/CASE02/results.json"),
    ]
    for source, destination in pairs:
        spec = importlib.util.spec_from_file_location(Path(source).stem, ROOT / source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.run()
        (ROOT / destination).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{result['case_id']}: wrote {destination}")


if __name__ == "__main__":
    main()
