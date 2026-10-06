# Verification record

Date: 2026-10-05 UTC. Release: 1.1.0-author-review. Author: Keshavan Thiagaraja.

## Executed checks

```sh
python -W error run_all.py
python -W error -m unittest discover -s tests -v
python verify_manifest.py
```

All 13 chapter labs and both additive ShopSmart worked cases passed. All 120 tests passed with warnings treated as errors: 55 original tests, 46 classical-learning tests and 19 added basket/forecast tests. Tests cover exact arithmetic, independent identities, finite differences, seeded metric contracts, disjoint partitions, training-only transforms, genuinely fitted calibration, deterministic reruns, strict budgets and infeasible plans. Three original SVG result charts were regenerated.

The final ZIP was extracted into a separate directory. Its manifest was verified before execution; the full runner and all 120 tests then passed in the extracted copy. All 13 individual chapter scripts and both added cases also ran from an unrelated working directory. A second manifest check after those runs found no source/result drift. Test logs were written outside the extracted package.

The 36 original files comprising Chapters 1–8 and `tests/test_labs.py` were compared byte-for-byte with the preserved 1.0.0 archive; all matched. The original archive was not overwritten. Its SHA-256 is recorded in RELEASE_NOTES.md. No dependency version was changed.

A basic scan for common credential/private-key patterns found no matches in the packaged text files. This is a limited precaution, not a comprehensive security or vulnerability audit.

## Verification boundaries

Not executed: a fresh dependency installation; Windows or macOS execution; real-data forecasting/classification; a production platform, voice/OCR, retailer or courier integration; live-price checking; checkout or purchasing; remote GitHub publication/access verification; dependency vulnerability auditing. The pinned packages were already present on the tested Linux/Python runtime.

The author has requested public code access, without purchase verification. Remote publication is a separate action and is not established by local test success. No reuse licence was selected on the author's behalf. This release is educational author-review material, not a production system or a publication-acceptance certificate.

## Interpretation of deliberate examples

- Chapter 8 retains deliberately invalid leakage examples. High leaked scores are not valid model evaluations.
- Chapter 11's fitted calibration uses a separate 250-row calibration partition and is tested not to refit the base scalers/models. It does not guarantee future calibration.
- Chapter 12 selects a family using validation, then refits development rows and evaluates each predeclared family once on held-out test data.
- Clustering/PCA results establish synthetic geometry, not customer meanings or causal explanations.
- ShopSmart basket/timing cases use wholly synthetic prices, fees, availability, eligibility and scenario probabilities. Voice/upload parsing, live product safety and fulfillment are not implemented.
