# V2C23-CASE01: Metrics with explicit labels and uncertainty

Release 0.1.0, Volume 2, Chapter 23. Synthetic teaching fixture.

## What the program does

supported=1 is a synthetic human evidence-support label. flagged_unsupported=1 is the detector prediction, so unsupported is the positive class for its confusion matrix. Calibration uses four separate confidence/outcome pairs. One bin deliberately hides opposing errors. The paired bootstrap resamples request indices once for both candidate and baseline.

## Interpret the result

Faithfulness is 0.7 with a Wilson 95% interval about [0.396778,0.892209]. Detector precision and recall are both 2/3. Brier score is 0.175 despite one-bin ECE rounding to zero. The paired improvement is 0.3 and its seeded percentile interval is [0,0.6]. These tiny synthetic labels do not validate factual truth or a deployed system.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 23 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter23.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
