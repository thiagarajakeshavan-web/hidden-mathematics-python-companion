# Volume 2 Python companion, author-review release 0.2.0

The Hidden Mathematics of Machine Learning and Large Language Models
Volume 2 of 2: Deep Learning, LLMs and Production AI Engineering
Author: Keshavan Thiagaraja

Fourteen small, offline laboratories correspond to Chapters 15–26. The same executable code serves the separate English and Tamil editions. Start with README_TA.md if you prefer Tamil guidance.

These are synthetic teaching demonstrations. They are not SHOP SMART AI production services, pretrained LLMs, retailer integrations, real allergy recommendations, purchases, deployed agents or performance benchmarks. No account, API key, GPU, live customer data or model download is required. The tests and case runners make no network calls. Some cases use controlled supplied numbers rather than learned models; each guide states the exact scope.

## Status and access

This downloadable package is prepared for author review. Public GitHub access is intended for everyone, including readers who do not buy the book, but publication and account setup remain pending. There is no verified public repository URL. No new licence for the author's work is granted by this package; the author's licence decision is pending. See RIGHTS_AND_DEPENDENCIES.md.

## Setup

Tested with CPython 3.12.14 and NumPy 2.3.5 on Linux x86_64. Other versions or operating systems were not validated in this release. Python 3.12 and a compatible NumPy wheel are the recommended starting point.

1. Extract the ZIP into a folder that you can read and write.
2. Open a terminal in the extracted folder containing this README and run_cases.py.
3. If Python and the pinned NumPy are already installed, proceed directly to the runs below. All cases then work offline.
4. If you need an isolated environment, create it using your trusted Python installation. The dependency installation step needs internet unless you already have a trusted local wheel. Only NumPy is installed; no model is fetched.

Linux, macOS or Ubuntu in Windows WSL:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.lock

Windows PowerShell using an already installed Python 3.12:

    py -3.12 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.lock

On Windows, substitute .\.venv\Scripts\python.exe for python in the commands below. These steps do not require changing PowerShell execution policy. Do not install packages from an unsolicited link or paste credentials into this companion. Python's official site is https://www.python.org/ and NumPy's official installation guide is https://numpy.org/install/.

## Run and check

Run every chapter and compare to its recorded result:

    python run_cases.py --verify

Write a fresh JSON result file:

    python run_cases.py --verify --output my_results.json

Run only Chapter 17:

    python run_cases.py --chapter 17 --verify

Run a case directly, from any current folder:

    python volume-02/edition-0.1.0/chapter-17/case-01/run.py

Run all tests:

    python -m unittest discover -s tests -v

The runner returns a nonzero exit status when a recorded result differs. It uses absolute and relative tolerances of 1e-9 for numeric output; exact equality is used for strings, booleans and result structure. This handles harmless floating-point tails such as 0.7000000000000001. The gradient tests have independent mathematical tolerances. The seeded bootstrap uses NumPy PCG64 with seed 23, 10,000 paired resamples, and linear percentile interpolation. Its interval is specific to this tiny synthetic fixture.

## Chapter map

| Case | What actually runs |
|---|---|
| V2C15-CASE01 | One ReLU hidden unit, sigmoid loss, analytical backpropagation, central differences, one simultaneous SGD step |
| V2C15-CASE02 | Two supplied scalar gradients through AdaGrad, uncentred RMSProp and bias-corrected Adam |
| V2C16-CASE01 | 1D cross-correlation, two recurrent steps, an LSTM cell with supplied gate values |
| V2C16-CASE02 | BatchNorm forward training/frozen inference and LayerNorm-axis comparison |
| V2C17-CASE01 | Scaled dot-product attention, causal masking, sinusoidal positions |
| V2C18-CASE01 | Supplied BPE merge rules, smoothed conditional counts, NLL/perplexity, synthetic power-law fit |
| V2C19-CASE01 | Two-candidate SFT step, reference-corrected DPO loss/derivatives, additive rank-one LoRA |
| V2C20-CASE01 | Exact cosine over lexical vectors, authorization/freshness filtering, separate restriction review gate |
| V2C21-CASE01 | Bounded deterministic workflow with callable mock read tools and no write tool |
| V2C22-CASE01 | Event-time and known-at selection, TTL, deduplication, conflict quarantine |
| V2C23-CASE01 | Label metrics, calibration counterexample, Wilson interval and paired bootstrap |
| V2C24-CASE01 | Symmetric int8 quantization, pruning, categorical student training and analytic memory estimates |
| V2C25-CASE01 | Trusted-fixture authority predicate, cohort metric gaps, conservative restriction gate, limited ASCII email redaction |
| V2C26-CASE01 | Distribution distance, error budgets, Little's law and assumed full-path latency arithmetic |

Each case directory includes fixture.json, expected.json, an independent run.py entry point and English/Tamil guidance. The shared, readable algorithm source is in src/volume2_companion/chapterNN.py. Unit tests are in tests/test_companion.py. reports/all_executed_results_0.2.0.json contains actual execution output, while reports/TEST_REPORT_0.2.0.md describes the tested environment and remaining limits. CASE_CONTRACTS.json maps the exact synthetic inputs, definitions and outputs into one file.

## Work through a lab

Read its guide and identify the units and assumptions. Run the unchanged case and inspect its output. Compare one intermediate result against the book by hand. Copy the fixture before changing it; record your changes separately. If you alter a fixture, --verify should fail until you independently validate the new result. Do not change expected.json just to hide an unexplained failure.

For Chapter 15, change the learning rate and observe when a single step stops helping. For Chapter 17, change only a future value and verify that the first causal output stays unchanged. For Chapter 22, move available_at past the decision time to expose why event_time alone leaks future knowledge. These are controlled learning experiments, not product claims.

## Safety and interpretation

A similarity score cannot establish truth or product eligibility. Current, complete, resolved restriction evidence only advances a synthetic example to human review; it never guarantees allergen safety. Missing, stale, conflicting or unresolved peanut cross-contact evidence blocks automatic eligibility. Peanuts and tree nuts are distinct. All health-like constraints belong to hypothetical shoppers, never to the author or a real user.

The authority flags in Chapter 25 are trusted test fixtures. In a real application they must come from authenticated application controls, never from model output or retrieved text. The Chapter 21 workflow ignores untrusted text by construction; it does not test an LLM's resistance to prompt injection. Its mock handlers cannot call a retailer, make a purchase or write external data. The email regular expression is deliberately incomplete and is not a general PII detection or privacy guarantee.

No source manuscripts, investor material, recovered conversations, real personal data or credentials are included in this package. No supplied external code was executed to produce these labs. All fixtures were independently implemented for this review release.

## Release 0.2.0 additions and preservation

This release contains 14 cases and 287 passing unittest methods: the original 226, 45 new bridge tests and 16 separately written reviewer oracles. The 12 original case directories remain byte-for-byte under edition-0.1.0; the two new CASE02 directories are under edition-0.2.0. The original 0.1.0 archive and historical execution reports remain distinct.

The default runner now includes all cases. --chapter 15 or --chapter 16 runs both cases in that chapter. To select just the new optimizer case:

    python run_cases.py --chapter 15 --case 2 --verify

The normalisation case uses --chapter 16 --case 2. Adding --case 1 selects the original cases. Existing direct CASE01 entry points retain their original meaning. Independent reviewer tests do not read expected output files. See reports/TEST_REPORT_0.2.0.md and reports/release_validation_0.2.0.json for actual release checks.

The new labs explain scalar optimizer updates and forward normalization only. There is no new neural-training benchmark or production claim. PyTorch documentation specifies comparison conventions; PyTorch is neither installed by this package nor used in its execution.
