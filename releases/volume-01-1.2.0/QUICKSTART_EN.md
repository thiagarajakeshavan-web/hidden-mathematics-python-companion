> Release 1.2.0 supplement: the preserved setup guidance below still applies. After setup, see [the new case guide](shopsmart_scenarios/README_EN.md), run `python run_additions.py`, and run the full suite (now 178 tests). Publication remains pending.

# English quickstart

This companion runs locally. The author has chosen public code access for everyone, without a book-purchase gate. Extract the supplied release ZIP or obtain the matching release from the author's verified public repository when available. This archive does not verify remote publication.

## 1. Prepare

Use Python 3.12. The recorded tests used Python 3.12.14. Python is available from its official site, https://www.python.org/downloads/ . Extract the ZIP into a folder you can write to. Open a terminal in the extracted `volume1_code` folder, where `requirements.txt` is visible.

The commands below create a project-local virtual environment. They do not change system Python, shell profiles or script-execution policies. Do not run as administrator/root. Do not type both platform sections.

## 2. Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_all.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Run just Chapter 1:

```powershell
.\.venv\Scripts\python.exe V1C01\lab.py
```

No virtual-environment activation or execution-policy change is necessary. If `py -3.12` is not found, check that Python 3.12 is installed before proceeding.

## 3. Linux or macOS terminal

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_all.py
.venv/bin/python -m unittest discover -s tests -v
```

Run just Chapter 1:

```sh
.venv/bin/python V1C01/lab.py
```

If your system does not supply `python3.12` or its virtual-environment support, install them through a trusted official route for your platform. Do not use `sudo pip` or change the system interpreter to work around the error.

## 4. Read the result

The complete runner reports one result path per chapter. Open `V1C01/results.json` through `V1C13/results.json` in a text editor. The full test run should end with `Ran 120 tests` and `OK`. Runtime and low-order numeric digits may vary. The included `test_report.txt` records the actual author-stage Linux run; it does not certify your installation.

To focus on one chapter's tests, use the same environment's Python executable followed by:

```sh
-m unittest discover -s tests -p test_labs.py -k V1C01 -v
```

## 5. Experiment safely

Keep an unmodified copy of the release. Change one variable in a copied folder and rerun. Do not replace held-out tests with training data, choose thresholds from final test outcomes, or interpret the deliberately leaked features as valid predictors. All supplied data is synthetic. Dependencies need a network connection during installation; the labs themselves do not.

## 6. Expanded Chapters 9–13

Release 1.1.0 adds learning paradigms (`V1C09`), regression (`V1C10`), naive Bayes/kNN/SVM (`V1C11`), trees/ensembles (`V1C12`) and clustering/PCA (`V1C13`). The same setup runs all thirteen labs. Chapter 14 is a book preview only, with no code lab.

For one new chapter, use your environment's Python executable in place of `python`:

```sh
python V1C11/lab.py
python -m unittest discover -s tests -p test_classical_labs.py -k V1C11 -v
```

For example, Linux/macOS full commands are `.venv/bin/python V1C11/lab.py` and `.venv/bin/python -m unittest discover -s tests -p test_classical_labs.py -k V1C11 -v`. On Windows use `.\.venv\Scripts\python.exe` instead.

The new 46 tests supplement the unchanged original 55. Chapter 11 uses distinct training, calibration and test rows. Chapter 12 selects its family on validation, not test. Chapter 13 fits standardization and PCA on training rows only. Fixed seeds and saved split indices support reproduction; these synthetic results do not establish product performance. All code stays outside the books.

To check package integrity before editing, run your environment's Python with `verify_manifest.py`. Recomputed outputs or intentional source edits may cause a checksum mismatch; keep an unchanged release copy.

## 7. Extra ShopSmart worked cases

The full runner also writes `shopsmart_examples/basket_results.json` and `shopsmart_examples/forecast_results.json`. They check a 27-assignment synthetic basket comparison (Chapter 5, CASE02) and a synthetic price forecast plus assumed buy-now/wait costs (Chapter 10, CASE02). Read `shopsmart_examples/README.md`. The extra 19 tests bring the total to 120. The fixed inputs do not implement typed/voice/upload recognition, real store quotes, orders or delivery integrations.
