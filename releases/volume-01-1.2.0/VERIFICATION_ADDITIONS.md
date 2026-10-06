# Verification record: 1.2.0 additions

Date: 2026-10-05 UTC. Author: Keshavan Thiagaraja. Release: 1.2.0-author-review.

## What actually ran

- All 178 unit tests passed with warnings treated as errors: the preserved 120 tests plus 58 new tests.
- The five new case scripts ran through `run_additions.py`, producing the included expected JSON.
- A separate clean copy ran the unchanged `run_all.py`: all thirteen chapter labs, both earlier ShopSmart cases and original mathematical charts completed. It then ran all five additions and the full 178-test suite again.
- After those clean-copy runs, all 85 inventoried original files still matched the recovered 1.1.0 baseline byte-for-byte. These include all prior source, input fixtures, saved results, charts and the three prior test modules. Only four existing release/navigation documents and the main inventory were intentionally updated in this release.
- Every Python file passed syntax/AST parsing. A limited scan for common private-key, GitHub-token and API-key shapes found no matches in packaged text. This is not a comprehensive security audit.
- An independent code review checked the exact-mask DP, adaptive expectation semantics, whole-pack budgets, allergen gates and nutrient/reference scope. Four validation edge cases were fixed and independently rechecked: unknown CSV cold-chain flags, missing fee fields, custom forecast horizons and silently changed nutrient attribution. Boolean numeric edge cases were also covered. The separately added finite No Free Lunch hook has four passing tests.

## Commands

From the companion root, using Python 3.12.14 and the already installed pinned dependencies:

```sh
python -W error run_all.py
python run_additions.py
python -W error -m unittest discover -s tests -v
python verify_preservation.py
python verify_manifest.py
```

The old runner was exercised in a separate copy to keep the recovered baseline untouched. Current outputs are in `full_extension_test_report.txt`, `extension_test_report.txt`, `addition_smoke_report.txt` and `legacy_runner_smoke_report_1.2.txt`. `TESTED_ENVIRONMENT_ADDITIONS.json` records the environment; `BASELINE_PRESERVATION.json` records original file hashes. The older files `TESTED_ENVIRONMENT.json`, `test_report.txt`, `smoke_report.txt` and `VERIFICATION.md` remain historical 1.1.0 evidence, not claims about the new case count.

## Important tested contracts

- Every one of seven nonempty store subsets is compared; an independent exhaustive oracle checks the DP on twelve small randomized instances.
- Whole packs, nonnegative integer cents, sufficient stock, explicit equivalence and route conditions are validated; unknown cold-chain CSV flags are rejected.
- The fixed 10/10/10 split does not constrain the optimum. Under original synthetic fees, ALDI-only A$109.20 wins; the optimized three-store basket costs A$111.00.
- Day-two and day-three expected decision costs are A$109.10 and A$105.88 after waiting penalties. Risk-neutral and minimax decisions differ. Infeasible positive-probability states are not discarded from an expectation.
- The full dinner kit for five costs A$32.80, including A$6.00 assumed fees. The strict-under-budget condition rejects equality. Missing mandatory fee fields are rejected rather than treated as free.
- Vegan status, peanut and separately named tree nuts are hard constraints. Unknown, missing, stale, conflicting and unresolved cross-contact evidence is excluded. Actual-product clearance always remains false.
- Four verified AFCD cooked-lentil nutrient values scale by an explicitly assumed cooked weight. Whole-meal totals remain unknown. Silently changing nutrient names, units, reference values or source attribution fails validation.
- MLE/MAP/mean and finite No Free Lunch arithmetic use exact fractions; unsupported boundary modes and invalid probabilities are rejected.

## Not established

No fresh dependency installation, Windows/macOS execution, production benchmarking, live retail data, retailer/courier integration, actual label or kitchen assessment, end-to-end voice/upload parsing, physical route optimization, calibrated price forecast, real purchase, whole-meal nutrient adequacy or clinical advice was performed. No public GitHub repository, release, account action or unauthenticated access was verified. GitHub access is postponed; this local preparation does not change that. No new licence was selected.

The model deliberately rejects unsupported nonzero minimum spend and membership rules. Real fulfillment, expiry, availability and health constraints require additional current evidence. This author-review package is an educational implementation, not proof of publication readiness or an operational ShopSmart service.
