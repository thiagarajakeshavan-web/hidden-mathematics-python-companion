# V1C10 · Linear and Logistic Regression

Primary case: `V1C10-CASE01` · Companion release: `1.1.0-author-review`

## Purpose and inputs

The exact regression fixture has four constructed `(distance km, duration minutes)` training pairs `(1,2),(2,3),(3,5),(4,4)` and two separate test pairs `(5,5),(6,7)`. The logistic fixture supplies coefficients `b=−2,w=0.8`; they are illustrative inputs, not fitted estimates. The CSV files mirror these fixtures.

The larger regression experiment uses 400 independent synthetic rows with distance, traffic index and pickup count. Its disclosed generator is `minutes=4+1.5*distance+8*traffic+0.4*pickup_count+Normal(0,2²)`. The classifier uses the shared fictional replenishment generator in `classical_common.py`. These isolated teaching models do not implement a courier integration or meal/basket planner.

## Run and test

```sh
python V1C10/lab.py
python -m unittest discover -s tests -p test_classical_labs.py -k V1C10 -v
```

Use the virtual environment's Python from the root quickstart. The lab writes `V1C10/results.json` independently of the current working folder.

## Expected mathematics

- OLS slope `0.8`, intercept `1.5`, training SSE `1.8`
- Two held-out predictions `5.5,6.3`: MAE `0.6`, RMSE `0.608276253`, R² `0.63`
- Training-mean baseline `3.5`: held-out MAE `2.5`, RMSE `2.692582404`
- At zero parameters and loss `SSE/(2n)`, gradients `db=−3.5,dw=−9.75`; learning rate `0.1` gives `b=0.35,w=0.975`, loss `0.49796875`
- Ridge objective `SSE+5*w²` with unpenalized intercept gives slope `0.4`, intercept `2.5`
- Supplied logistic probabilities `0.231475217,0.5,0.768524783`, mean log loss `0.406570705` nats

## Executed held-out experiments

| Experiment | Split and seed | Model result | Baseline result |
|---|---|---|---|
| Synthetic duration regression | 300 train / 100 test; seed 1010 | MAE 1.587100462, RMSE 1.936384274 | Training-mean MAE 8.157528297, RMSE 9.504236603 |
| Synthetic replenishment classification | 600 train / 200 test; seed 1011 | Accuracy .77, AUC .858985899, log loss .469854444, Brier .153847279 | Training-prior accuracy .505, AUC .5, log loss .693119403, Brier .249986111 |

Both scalers fit only training rows. Model choices are fixed in advance: ordinary least squares; logistic regression `C=1`, `max_iter=2000`; classification threshold `0.5`. There is no hyperparameter or threshold selection from the final test set. Classification uses a stratified split; regression uses an independent random split. Full split indices and full-precision results are included in JSON.

## Interpretation and experiment

The regression generator deliberately has linear structure, so this favorable result is expected. One synthetic IID split is not evidence about future traffic, correlated journeys or operational delivery times. Proper scores assess more than calibration; fitted logistic probabilities are not automatically well calibrated. Experiment with a nonlinear regression generator or a changed noise level in a copy; preserve an untouched test set and never describe that experiment as a measured ShopSmart improvement.
