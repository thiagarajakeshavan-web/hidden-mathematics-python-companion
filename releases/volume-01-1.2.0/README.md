# Volume 1: Mathematical Foundations and Classical Machine Learning — Python Companion

Author: **Keshavan Thiagaraja**  
Release: **1.2.0-author-review** · Executable Chapters 1–13 · English and Tamil editions

This is the separate executable companion to the expanded Volume 1. The book also includes a brief Chapter 14 preview; there is intentionally no Chapter 14 code lab. The approved two-volume series continues with full Chapters 15–26 in Volume 2. No Python listing belongs in either book manuscript. One tested source serves both language editions.

Start with [QUICKSTART_EN.md](QUICKSTART_EN.md) or [QUICKSTART_TA.md](QUICKSTART_TA.md). For the five new teaching cases, read [the English guide](shopsmart_scenarios/README_EN.md) or [the Tamil guide](shopsmart_scenarios/README_TA.md). The author has chosen public code access for everyone, with no book-purchase gate. Repository publication is handled separately; this archive does not itself establish that a remote repository or release has been published.

## What is included

| Chapter | Folder | Cases | What the experiment establishes |
|---|---|---|---|
| 1 · Linear Algebra | V1C01 | V1C01-CASE01 | Signed cosine, a linear system, eigendecomposition, SVD and PCA reconstruction |
| 2 · Calculus | V1C02 | V1C02-CASE01 | Chain rule, numerical gradient checks and simultaneous network updates |
| 3 · Probability | V1C03 | V1C03-CASE01 | Base-rate Bayes arithmetic, distributions, expectation and conjugate updating |
| 4 · Statistics | V1C04 | V1C04-CASE01/02 | Small-sample t inference, MLE and separate LLN/CLT simulations |
| 5 · Optimization | V1C05 | V1C05-CASE01/02/03/04 | Normalized loss, stable/unstable rates and conditioning |
| 6 · Information Theory | V1C06 | V1C06-CASE01 | Entropy, cross-entropy, KL identity and stable softmax |
| 7 · Learning Theory | V1C07 | V1C07-CASE01/02 | Exact bias–variance decomposition, finite-class bounds and held-out regularization |
| 8 · Evaluation Metrics | V1C08 | V1C08-CASE01 | Confusion metrics, ROC/PR, calibration, cost and leakage evidence |
| 9 · Types of Machine Learning | V1C09 | V1C09-CASE01 | Supervised error, clustering updates, masked-token loss and simulated RL arithmetic |
| 10 · Linear and Logistic Regression | V1C10 | V1C10-CASE01/02/03 | OLS, ridge, gradients, logistic probabilities and held-out baseline comparisons |
| 11 · Naive Bayes, kNN and SVM | V1C11 | V1C11-CASE01 | Bayes smoothing, distance scaling, margins and separately fitted calibration |
| 12 · Trees and Ensembles | V1C12 | V1C12-CASE01/02/03 | Split gains, a residual-boosting step and validation-selected model comparison |
| 13 · Clustering and Dimensionality Reduction | V1C13 | V1C13-CASE01/02 | K-means geometry, PCA and training-only transformation of held-out rows |

Chapter labels are navigation aids; the book's chapter/case identifiers are authoritative. `V1Cxx-LAB01` identifies additional experiments where used by the original chapters. Each folder contains source, guidance, saved results and readable input fixtures where useful. `run_all.py` refreshes all 13 result files and the three original mathematical SVG charts.

## Added ShopSmart worked cases

`shopsmart_examples/` adds `V1C05-CASE02` (27-assignment whole-pack basket/fee comparison) and `V1C10-CASE02` (tiny synthetic price regression plus a separate assumed buy-now/wait decision). These are included in the full runner without changing the original Chapter 5 lab. See [the case guide](shopsmart_examples/README.md) for exact inputs, results, uncertainty and limits. Typed, voice and upload adapters are proposed only; no live retailer, nutrition, purchasing or courier pipeline is implemented.

## New 1.2.0 teaching extensions

`shopsmart_scenarios/` adds V1C05-CASE03 (30-line whole-pack optimization over all seven store subsets), V1C10-CASE03 (day 0/2/3 decisions under explicit fictional scenarios) and V1C05-CASE04 (one complete synthetic vegan cooking kit for five at A$32.80 including assumed fees). These cases distinguish the fixed 10/10/10 illustration from the optimizer’s allocation, unknown allergen evidence from eligibility, and cooked-lentil reference calculations from unknown whole-meal nutrition. V1C04-CASE02 adds exact MLE/MAP arithmetic; V1C07-CASE02 adds a bounded finite No Free Lunch illustration.

Run `python run_additions.py` to refresh only these five additions. The original `run_all.py`, original chapter source/fixtures/results/charts and original three test modules remain unchanged. Read [VERIFICATION_ADDITIONS.md](VERIFICATION_ADDITIONS.md) for the current check record and [BASELINE_PRESERVATION.json](BASELINE_PRESERVATION.json) for preserved-file hashes. The older verification logs and environment file are explicitly retained as historical 1.1.0 records.

## Reproducibility and interpretation

- All learning fixtures and commercial/eligibility assumptions are constructed or seeded synthetic data. The new dinner example additionally uses four explicitly sourced FSANZ reference nutrient values for cooked, drained lentils. No real customer, employer, personal, investor or proprietary dataset is included.
- ShopSmart is the proposed B2C/B2B scenario. These are isolated mathematical teaching labs, not an implemented or tested shopping, nutrition, allergen, multi-store, courier or purchasing pipeline. No benchmark against Amazon or another live product was performed.
- Small exact examples and larger measured synthetic experiments are distinguished explicitly. Seeded outcomes are not operational performance claims. Cross-chapter scores from different data/splits are not a common benchmark.
- `requirements.txt` preserves the tested pinned package versions. Linux x86-64 / Python 3.12.14 executed all 13 labs and **178 tests**: the existing 120 plus 58 new grocery, timing, dietary-constraint, nutrient-scaling, MAP/MLE and finite No Free Lunch tests. Tests treat warnings as errors. Windows/macOS execution and a fresh dependency installation were not run.
- Original Chapter 1–8 source, fixtures, results, charts and original 55-test module remain byte-for-byte unchanged from the 1.0.0 archive. Their chapter READMEs retain that original content-version label. Root tooling and guidance are updated for the expanded release.
- New split-isolation tests verify disjoint partitions and training-only fitted scaling/PCA. Chapter 11 fits genuine sigmoid calibrators on rows never seen by the base models. It does not present a raw sigmoid of an SVM margin as calibrated probability.
- Chapter 12 selects the family using validation log loss, then refits on development rows before final testing. On this largely linear synthetic fixture the logistic baseline wins; ensembles are not assumed superior.
- Chapter 7 selects its ridge parameter using validation. Chapter 8 deliberately includes invalid leakage examples and a retrospective threshold-cost calculation. Those teaching examples are not valid deployment-selection procedures.
- Floating-point tests use tolerances. Fixed seeds establish repeatability in the recorded environment, not bit-identical outputs on every numerical library or device.

## Local workflow

1. Read the relevant mathematics in the book.
2. Open the matching README and inputs.
3. Run a chapter or all labs; inspect the saved JSON.
4. Run tests and change one documented parameter at a time in a copy.
5. Interpret results against assumptions. Protect held-out data, feature availability and the distinction between prediction and decision.

The scripts compute locally and write companion result files. They do not download data, sign in, purchase, publish, send telemetry, alter shell profiles or configure cloud accounts. Dependency installation uses the reader's configured package source. The output helper sets a process-local default `LOKY_MAX_CPU_COUNT=1` to avoid unreliable physical-core discovery in small containers; it does not change the operating system or the reader's shell configuration.

## Public access and rights

The author has requested public code availability without purchase verification. This release contains no manuscripts or confidential project/investor sources. Public availability is not a separate open-source licence grant: no new commercial licence, reuse licence or distribution terms have been selected on the author's behalf. Dependency licences apply to those dependencies; see [DEPENDENCIES.md](DEPENDENCIES.md). The companion does not bundle dependency binaries.

## Verification records

- `TESTED_ENVIRONMENT_ADDITIONS.json`: current 1.2.0 runtime and scope
- `full_extension_test_report.txt`: current full 178-test output
- `extension_test_report.txt`: 58 new-case tests
- `addition_smoke_report.txt`: five new case scripts
- `VERIFICATION_ADDITIONS.md`: current clean-copy and preservation checks
- `DATA_PROVENANCE_ADDITIONS.md`: new synthetic inputs and scoped reference nutrient values
- `TESTED_ENVIRONMENT.json`: historical 1.1.0 runtime versions and verified/unverified scope
- `test_report.txt`: full 120-test output
- `smoke_report.txt`: all-lab runner output
- `VERIFICATION.md`: commands, original-content preservation and archive checks
- `MANIFEST.json`: per-file SHA-256 inventory; `verify_manifest.py` checks it
- `DATA_PROVENANCE.md`: fixtures, seeds and data boundaries
- `RELEASE_NOTES.md`: changes from the original 1.0.0 archive

If a result changes after an intentional edit, reconcile the code, fixtures, tests, saved results and both book editions together. Never change expected values merely to conceal a regression.
