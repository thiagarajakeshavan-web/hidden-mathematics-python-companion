# Release 1.2.0-author-review

Author: Keshavan Thiagaraja. Prepared 2026-10-05 UTC. Five additive cases: V1C04-CASE02, V1C05-CASE03, V1C05-CASE04, V1C07-CASE02 and V1C10-CASE03. All prior chapter source, fixtures, results, charts and three prior test modules are preserved byte-for-byte. New standard-library code, explicit fixtures, saved JSON, English/Tamil guides and 58 tests extend the prior 120-test suite to 178. Current verification is in VERIFICATION_ADDITIONS.md. The older release record follows unchanged. No remote publication or new licence grant is implied.

# Release 1.1.0-author-review

Author: Keshavan Thiagaraja. Expanded Volume 1 companion: Chapters 1–13. Chapter 14 remains a book-only preview, with no code lab. The approved series has two volumes, with Volume 2 covering full Chapters 15–26.

## Added

- Five chapter labs, fixed CSV fixtures and explanatory READMEs
- Linear/logistic held-out baseline comparisons
- Naive Bayes/kNN/SVM comparison with genuinely separate calibration data
- Tree/forest/boosting comparison using validation for family selection
- Training-only scaling, PCA and cluster assignment on held-out synthetic data
- 46 numerical, reproducibility, split-isolation, calibration and edge-case tests
- Two added ShopSmart worked cases (basket-fee enumeration and synthetic forecast/timing), with 19 further tests; total 120 tests
- English/Tamil expanded quickstart guidance, `.gitignore` and manifest verification

## Preserved

The original eight chapter folders and `tests/test_labs.py` are byte-identical to the previous ZIP, including saved results and charts. The previous ZIP is retained separately and is not overwritten. Root tooling now runs 13 labs. Existing pinned dependency versions are unchanged. No manuscript code listings, third-party data, credentials or dependency binaries were added.

Original archive SHA-256:
`b2d355c830c176401f54aa21a113824cd6943e07cf215284d6e93218f5f46b3b`

## Access choice

The author has requested public code access for everyone, without purchase verification. No open-source/commercial licence terms were selected on the author's behalf. Publishing and remote access verification are separate from local package testing.
