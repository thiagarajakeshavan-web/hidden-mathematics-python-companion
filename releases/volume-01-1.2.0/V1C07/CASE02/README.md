# V1C07-CASE02: a finite No Free Lunch illustration

Author: Keshavan Thiagaraja. Additive release 1.2.0-author-review.

Let X = {a,b}; observe f(a)=0. Under uniform weighting of all binary target functions, two targets remain: (0,0) and (0,1). Always predicting 0 at b and always predicting 1 at b each have mean unseen 0–1 error 1/2. A randomized prediction with probability q of predicting 1 also has error (1/2)q+(1/2)(1−q)=1/2.

The equality comes from fixed observed data and symmetric weighting of the remaining labels. It does not describe the distribution of real shopping data or imply practical algorithms always tie. Structured tasks and useful inductive biases matter. This tiny enumeration is an illustration, not a general theorem proof or benchmark.

From the companion root, run `python V1C07/CASE02/no_free_lunch.py` and read `results.json`. Tests are in `tests/test_shopsmart_scenarios.py`. Original Chapter 7 source, inputs and results are unchanged.
