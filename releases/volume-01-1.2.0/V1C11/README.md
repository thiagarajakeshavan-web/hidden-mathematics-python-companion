# V1C11 · Naive Bayes, kNN and SVM

Primary case: `V1C11-CASE01` · Companion release: `1.1.0-author-review`

## Purpose and inputs

Constructed marginal counts teach Bernoulli naive Bayes: 10 late and 30 on-time cases; congestion positives 8/6 and prior-delay positives 6/3. Three constructed two-feature points teach distance scaling. Four signed points teach the support-vector margin. CSVs mirror all fixtures. A larger independent synthetic replenishment dataset tests the three classifier families under the same split and calibration protocol.

## Run and test

```sh
python V1C11/lab.py
python -m unittest discover -s tests -p test_classical_labs.py -k V1C11 -v
```

Use the environment's Python from the root quickstart. Tests check frozen-model identity, training-only scaling and a genuinely fitted calibrator. Applying a raw sigmoid to an SVM margin is not the calibration workflow used here.

## Expected mathematical results

- Two-positive Bernoulli NB posterior `8/9`; feature smoothing `alpha=1` gives `16/19`, keeping empirical class priors unchanged
- Query `[2,100]` has raw distances `100,2,sqrt(6401)` and predefined-scale distances `1,2,sqrt(1.64)`; nearest label changes from `0` to `1`; three-neighbor positive vote fraction `2/3`
- Linear SVM on `x=[−2,−1,1,2], y=[−1,−1,1,1]` gives `w=1,b=0`, support vectors `−1,1`, margin width `2`
- Hinge loss for label `−1` and score `.2` is `1.2`; RBF for gamma `.5` and squared distance `2` is `exp(−1)`
- Idealized cost threshold `2/(2+8)=.2`, under calibrated probabilities and the chapter's stated decision-cost assumptions

## Executed comparison

Seed `1111`; 1,000 fictional product-period rows; 500 base-training / 250 calibration / 250 final-test rows. Every classifier gets the same rows and features. The split is stratified and disjoint. Inputs are stock-cover days, demand index, promotion flag and lead time; target is a simulated next-period replenishment flag.

- Gaussian NB uses its stated Gaussian/conditional-independence assumptions; the hand-worked NB fixture instead uses Bernoulli features.
- kNN uses training-only `StandardScaler`, 15 neighbors and uniform votes.
- SVM uses training-only `StandardScaler`, RBF kernel, `C=1`, `gamma='scale'`.
- Each fitted base model is wrapped in `FrozenEstimator`, then a fitted sigmoid calibrator uses only the 250 calibration rows. Base fitting and scaling never see those rows or final test rows.
- Threshold `.5` and all parameters are fixed beforehand. No model or threshold is chosen from final test scores.

| Model | Test accuracy | Test log loss, nats | Test Brier |
|---|---:|---:|---:|
| Calibrated Gaussian NB | .812 | .447109281 | .143027288 |
| Calibrated kNN | .744 | .472071356 | .153533213 |
| Calibrated RBF SVM | .800 | .470476613 | .150585097 |
| Training-prevalence baseline | .516 | .692635093 | .249744000 |

The simple baseline uses training labels only; each calibrated classifier additionally uses the separate calibration labels. Uncalibrated NB/kNN probability metrics are included in JSON for comparison. SVM margins are reported as scores, not probabilities.

## Interpretation and experiment

This one-seed IID comparison is not a universal model ranking. Calibration fitting neither guarantees calibration nor guarantees a lower final test loss. Brier/log loss are proper scores, not pure calibration measures. Vary training size or a predeclared parameter on a fresh development split; protect the final test. No feature here determines dietary eligibility or allergen safety.
