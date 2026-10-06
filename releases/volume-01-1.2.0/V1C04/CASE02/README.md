# V1C04-CASE02: MLE, MAP and posterior mean

Author: Keshavan Thiagaraja. Additive release 1.2.0-author-review.

Seven successes in ten constructed Bernoulli trials give MLE = 7/10. An illustrative Beta(2,2) prior produces Beta(9,5), interior MAP = 2/3 and posterior mean = 9/14. A uniform Beta(1,1) prior gives MAP = MLE for these observations. These are distinct estimators; prior choice does not establish predictive superiority. The interior Beta(a,b) mode formula requires a,b > 1. This small hook rejects boundary cases rather than applying the wrong formula.

Run from the companion root: `python V1C04/CASE02/map_mle.py`. Read `results.json`. Tests are in `tests/test_shopsmart_scenarios.py`. No original Chapter 4 source, input or result was changed. English and Tamil guidance: `shopsmart_scenarios/README_EN.md` and `shopsmart_scenarios/README_TA.md`.
