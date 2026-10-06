# Dependencies and primary documentation

The pinned packages were already available in the test environment. They are not bundled in this ZIP. Installation requires access to your configured Python package index. This release makes no claim that these versions are the latest.

| Package | Tested version | Purpose | Upstream licence reference |
|---|---|---|---|
| NumPy | 2.3.5 | Arrays, random generation, linear algebra | https://github.com/numpy/numpy/blob/v2.3.5/LICENSE.txt |
| SciPy | 1.17.0 | Distributions, t inference, log-sum-exp | https://github.com/scipy/scipy/blob/v1.17.0/LICENSE.txt |
| scikit-learn | 1.8.0 | Metrics, splits, regression and validation | https://github.com/scikit-learn/scikit-learn/blob/1.8.0/COPYING |
| joblib | 1.5.3 | scikit-learn runtime dependency | https://github.com/joblib/joblib/blob/1.5.3/LICENSE.txt |
| threadpoolctl | 3.6.0 | Numerical thread-pool runtime dependency | https://github.com/joblib/threadpoolctl/blob/3.6.0/LICENSE |

Dependency licences and compiled-library notices apply to those dependencies, not automatically to the author's companion source. Review their actual distribution notices before redistributing dependency binaries.

Primary API documentation consulted on 2026-10-05:

- NumPy symmetric eigendecomposition: https://numpy.org/doc/stable/reference/generated/numpy.linalg.eigh.html
- NumPy SVD: https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html
- SciPy one-sample t test: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
- SciPy log-sum-exp: https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html
- scikit-learn metrics: https://scikit-learn.org/stable/modules/model_evaluation.html
- scikit-learn cross-validation and grouped data: https://scikit-learn.org/stable/modules/cross_validation.html
- scikit-learn leakage guidance: https://scikit-learn.org/stable/common_pitfalls.html

The online “stable” manuals can move to newer versions. The actual installed API and numerical tests, recorded in TESTED_ENVIRONMENT.json and test_report.txt, establish what this release executed.

Expanded Chapters 9–13 additionally use the existing pinned scikit-learn package for KMeans, PCA, logistic regression, naive Bayes, kNN, SVC, calibration, trees and ensembles. No deep-learning package or additional dependency was introduced. The installed 1.8.0 `FrozenEstimator` API was executed and tested; it preserves each base classifier while a sigmoid calibrator fits a separate partition.

Additional primary documentation checked on 2026-10-05:

- Probability calibration and disjoint base/calibration data: https://scikit-learn.org/stable/modules/calibration.html
- Clustering and limitations of cluster evaluation: https://scikit-learn.org/stable/modules/clustering.html

The online manuals currently resolve to a newer release than the pinned runtime. Runtime tests, not an assumption about the current stable API, establish compatibility with the versions in this package.
