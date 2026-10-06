# V2C17-CASE01: Causal attention with visible dimensions

Release 0.1.0, Volume 2, Chapter 17. Synthetic teaching fixture.

## What the program does

Q and K both have two features, so the dot products are divided by sqrt(2). A causal mask allows only keys whose position is no later than the query. Masked entries receive exactly zero weight, and each attention row sums to one. The value vectors have two output features. Sinusoidal encoding uses alternating sine/cosine pairs.

## Interpret the result

The first causal output is exactly [2,0]. The second is approximately [0.6604769013,2.6790461973]. Change the future value vector and verify that the first output cannot change. These weights express a computation, not a faithful explanation or evidence of truth.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 17 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter17.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
