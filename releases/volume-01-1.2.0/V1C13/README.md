# V1C13 · Clustering and Dimensionality Reduction

Cases: `V1C13-CASE01` k-means; `V1C13-CASE02` PCA · Release `1.1.0-author-review`

## Purpose and inputs

The six-point clustering fixture is `(0,0),(0,2),(2,0),(8,8),(8,10),(10,8)`. The separate rank-one PCA fixture is `(−2,−2),(−1,−1),(1,1),(2,2)`. CSVs mirror these coordinates. They are abstract geometric examples, not identified customers or validated customer groups.

## Run and test

```sh
python V1C13/lab.py
python -m unittest discover -s tests -p test_classical_labs.py -k V1C13 -v
```

Use the root quickstart's environment Python. Exact results and a separate training/test transformation experiment are written to `results.json`.

## Exact results

- Two centers are `(2/3,2/3)` and `(26/3,26/3)`; within-cluster sum of squares is `32/3`.
- A new point `(1,1)` has squared distances `2/9` and `1058/9`.
- A single center has total WCSS `608/3`. Lower distortion with more centers alone is not a criterion for choosing the number of meaningful groups.
- PCA uses sample covariance with denominator `n−1=3`; all entries are `10/3` and eigenvalues are `20/3,0`.
- One canonical leading direction is `(1/sqrt(2),1/sqrt(2))`; projected scores are `−2sqrt(2),−sqrt(2),sqrt(2),2sqrt(2)`.
- Rank-one reconstruction matches the inputs to floating-point precision. The sign of a PCA direction can reverse with no change in reconstruction or explained variance.

## Separate held-out transformation experiment

Seed `1313` generates 360 synthetic rows from three activity clouds with unequal feature scales. Split: 270 training / 90 test rows. `StandardScaler`, two-component PCA and three-center k-means all fit only training rows. The test set is transformed and assigned using those fitted objects. Results include training explained variance, test reconstruction MSE per standardized coordinate, test mean squared distance, silhouette and cluster counts.

Three clusters and two PCA components are fixed teaching choices, not test-selected quantities. The one-center comparator uses the training mean. The latent generator index is never used to fit models or give business names to clusters. These synthetic coordinates are not actual prices, nutritional measurements or customer spending.

## Interpretation and experiment

Low reconstruction error does not prove task usefulness. Large variance need not contain the feature signal required by a later predictor. A favorable silhouette does not establish stable customer segments or causal explanations. Try an alternative feature scale on a copy, then compare distortion and silhouette while describing the changed geometry. Manifold methods are discussed conceptually in the chapter; this lightweight release intentionally implements k-means and PCA only, with no nonlinear manifold lab or deep-learning dependency.
