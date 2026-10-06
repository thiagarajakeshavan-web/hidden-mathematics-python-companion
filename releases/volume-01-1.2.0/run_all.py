"""Run all thirteen labs and refresh their results; never installs or downloads data."""
from pathlib import Path
import importlib.util
import json
from common import ROOT, plain

def main():
    for number in range(1,14):
        chapter = f"V1C{number:02d}"
        spec = importlib.util.spec_from_file_location(chapter, ROOT/chapter/"lab.py")
        lab = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lab)
        result = plain(lab.run())
        path = ROOT/chapter/"results.json"
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+"\n",encoding="utf-8")
        print(f"{chapter}: wrote {chapter}/results.json")
    for source, destination in [
            ("shopsmart_examples/basket_comparison.py", "shopsmart_examples/basket_results.json"),
            ("shopsmart_examples/forecast_timing.py", "shopsmart_examples/forecast_results.json")]:
        spec = importlib.util.spec_from_file_location(Path(source).stem, ROOT/source)
        case = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(case)
        result = plain(case.run())
        (ROOT/destination).write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")
        print(f"{result['case_id']}: wrote {destination}")
    from generate_visuals import main as generate_visuals
    generate_visuals()

if __name__ == "__main__":
    main()
