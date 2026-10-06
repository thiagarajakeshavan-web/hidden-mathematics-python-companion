# V1C12 · Decision Trees, Random Forests and Gradient Boosting

Cases: `V1C12-CASE01` classification split; `V1C12-CASE02` squared-error boosting; `V1C12-CASE03` held-out comparison · Release `1.1.0-author-review`

## Purpose and inputs

A 12-row constructed classification fixture has four rows at `x=0`, all negative, and eight rows at `x=1`, six positive. A four-row regression fixture has `x=[0,1,2,3],y=[2,4,8,10]`. The larger comparison uses the same disclosed type of synthetic replenishment data as Chapters 10 and 11, with a different seed and a completely separate dataset. Do not compare scores across those different test sets as if they were a single benchmark.

## Run and test

```sh
python V1C12/lab.py
python -m unittest discover -s tests -p test_classical_labs.py -k V1C12 -v
```

Use the quickstart's environment Python. The lab writes the exact fixtures, validation scores, chosen family and final test comparison to `results.json`.

## Exact results

The fitted classification stump splits at `.5`. Parent Gini `.5`, weighted child Gini `.25`, gain `.25`. Entropy decreases from `1` to `.5408520829727552` bits, a gain of `.4591479170272448` bits. Left/right positive probabilities are `0,.75`. Cost-complexity expressions `.5+alpha` and `.25+2*alpha` tie at `alpha=.25`.

For regression boosting, initial prediction `6` gives residuals `−4,−2,2,4`; a stump at `1.5` predicts `−3,−3,3,3`. Learning rate `.5` gives predictions `4.5,4.5,7.5,7.5`, lowering MSE from `10` to `3.25`. Learning rate `1` gives `3,3,9,9`, MSE `1`. These are squared-error residual updates, not a description of logistic classification boosting.

## Fair comparison protocol

Seed `1212`; 800 IID synthetic rows; 480 training / 160 validation / 160 final test. Features are stock-cover days, demand index, promotion flag and lead time; target is a simulated replenishment flag. The generator's main effects are linear in log odds, with a small disclosed interaction. All models use identical features and row partitions.

Fixed candidates, defined before test evaluation:

| Family | Fixed configuration |
|---|---|
| Logistic baseline | Training-only standardization; C=1; max_iter=2000 |
| Decision tree | max_depth=4; min_samples_leaf=12 |
| Random forest | 80 trees; max_depth=5; min_samples_leaf=6; max_features=sqrt; n_jobs=1 |
| Gradient boosting | 100 stages; max_depth=2; learning_rate=.05; min_samples_leaf=8 |

There is no within-family tuning. Lowest validation log loss selects the logistic family. After that choice, each prespecified family is refitted on the same 640 development rows, including any preprocessing. A training-prior baseline is fitted on those rows too. Each final model is evaluated once on the 160 untouched test rows; test scores do not revise the selected family.

Test log losses are approximately `.443258` for logistic, `.719449` for the tree, `.469111` for the forest, `.478138` for boosting and `.693089` for the prior. Full precision, accuracy, AUC, average precision, Brier and confusion counts are in JSON.

## Interpretation and experiment

The more complex model does not automatically win. A largely linear synthetic generator is favorable to logistic regression; one split cannot establish production superiority. Small tree leaves can yield extreme probabilities and large log-loss penalties. No tree path, importance score or cluster label is a causal explanation. Repeat with prespecified alternative generators, seeds and development-only selection; retain an untouched test for each planned comparison.
