# Volume 2 companion test report: 0.2.0

Author-review edition. Author: Keshavan Thiagaraja.
Execution date: 6 October 2026 UTC.

## Actual result

- All 14 offline teaching cases executed and matched recorded outputs.
- All 287 unittest methods passed with Python warnings treated as errors: the original 226 methods, 45 new bridge tests, and 16 additional independently written reviewer checks.
- The original 226 comprise 208 core methods and 18 independent mathematical/behavioral oracles. Combined totals are 253 core/bridge methods and 34 independent reviewer methods. Subtests and loops are not counted as extra methods.
- The 12 original CASE01 directories and all pre-existing reports remain byte-for-byte unchanged. Their original paths deliberately retain edition-0.1.0. The two new CASE02 directories use edition-0.2.0.
- No GitHub publication, new licence, credential handling, model download, network data retrieval or production deployment was performed.

The tested runtime is CPython 3.12.14, NumPy 2.3.5, Linux x86_64. See environment.json for platform details. The pinned NumPy was already installed; no clean dependency installation or operating-system portability test was performed.

## New numerical evidence

### V2C15-CASE02: adaptive scalar updates

The case uses the same prescribed scalar gradient sequence (2, −1), parameter 0, learning rate 0.1, beta1=beta2=0.9 and epsilon=1e-8. Accumulators start at zero. Epsilon is outside the square root for all three methods; RMSProp is uncentred with no momentum or bias correction; Adam uses both zero-state bias corrections. No decay, clipping, schedule, AdamW or AMSGrad is included.

Final parameters:

- AdaGrad: −0.05527864015000421
- RMSProp: −0.16878580703585389
- Adam: −0.1270604029857565

Tests derive first and second updates from independent closed forms, including Adam corrected moments 8/19 and 46/19 at step two. Independent reviewer checks use 60-digit Decimal calculations and a mixed-gradient sequence. Tests discriminate outside-root epsilon from an incorrect inside-root expression, verify zero gradients and retained Adam direction, and reject invalid controls, nonfinite inputs and unrepresentable squared gradients.

These are arithmetic traces, not a comparison of trained models. A real training loop recomputes gradients at its own current parameters; different optimisers generally need not receive the same later gradients.

### V2C16-CASE02: BatchNorm and LayerNorm

Batch [[1],[3]], gamma=2, beta=0.5, epsilon=1e-5 gives mean 2, biased forward variance 1 and output [−1.499990000075, 2.499990000075]. The normalised variance is 1/1.00001, not exactly one.

The PyTorch-style running-stat demonstration uses update weight 0.1, initial mean 0 and variance 1. Only this running-variance update uses the unbiased batch variance 2, giving new running mean 0.2 and variance 1.1.

A separate inference comparison explicitly supplies frozen mean 1 and variance 4. It does not use the just-updated statistics. Inference outputs are [0.5, 2.499997500005]. Tests verify input-stat immutability, single-example inference, batch-composition independence at inference and composition dependence in training.

For the two-feature axis fixture [[1,3],[5,7]], BatchNorm column means are [3,5] with variances [4,4]; LayerNorm row means are [2,6] with variances [1,1]. Tests independently calculate both transforms, constant batches, single-feature LayerNorm, inside-root epsilon, invalid shapes, negative running variance and nonfinite/overflow rejection. Training requires at least two examples because its unbiased running-variance update is undefined with one.

This is forward-only arithmetic. No backward derivative, automatic differentiation, learned affine parameters, neural training benchmark, distributed statistic synchronisation or framework execution is implemented. PyTorch documentation informs conventions; PyTorch is not a package dependency or a tested runtime here.

## Retained regression coverage

The complete existing suite remains active. It covers the neural chain rule and finite differences; cross-correlation/RNN/LSTM; causal attention; tokenizer/count-language-model mechanics; SFT/DPO/LoRA; access-first retrieval and conservative restriction review; bounded mock-agent workflow; point-in-time known-at filtering; evaluation metrics and bootstrap; quantisation/pruning/distillation; trusted policy fixtures; and serving/monitoring arithmetic.

The original reports/TEST_REPORT.md describes those checks and their limits for release 0.1.0. It is historical evidence rather than the current count. Old executed results and tests were preserved instead of regenerated to disguise changes.

## Reproducibility and packaging

From the extracted package root:

    python -W error -m unittest discover -s tests -v
    python run_cases.py --verify
    python verify_manifest.py

The default runner now selects all 14 cases. Select the original cases with --case 1, or the two new cases with --case 2. Chapter 15 and Chapter 16 now each contain two cases. Existing direct CASE01 entry points still execute only their original case; every CASE02 directory has its own direct entry point.

The release validation JSON records socket-blocked execution, direct entry points from an unrelated directory, UTF-8/byte-compilation checks, preservation hashes and fresh archive extraction verification. Unit and archive checks have separate logs. SHA-256 checks establish byte integrity, not publisher identity or security certification. Source reference links were checked; public GitHub publication and the author's licence selection remain pending.

## Limits

Tests cannot prove absence of every bug or establish convergence, accuracy gains, business outcomes, deployment safety, privacy completeness or a production benchmark. Fixtures contain synthetic teaching values only. No customer, retailer, health, credential or investor data are included. Windows/macOS, other Python/NumPy versions, GPUs, clean installation, operational recovery and real deployment were not tested. No performance timing claim is made from test-suite elapsed times.
