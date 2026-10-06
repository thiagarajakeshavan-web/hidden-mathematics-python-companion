# V2C25-CASE01: A conservative policy predicate, not a security guarantee

Release 0.1.0, Volume 2, Chapter 25. Synthetic teaching fixture.

## What the program does

A request is allowed only when the action is read_catalogue and all trusted authorization, role and argument checks are strictly true, while sensitive export is strictly false. Strings such as true do not grant permission. Denial reasons are reported. Abstract cohort confusion counts produce TPR, FPR, accuracy and group sizes; they do not decide anyone’s eligibility.

## Interpret the result

Group A has TPR 0.8 and FPR 0.2; group B has TPR 0.6 and FPR 0.1. These gaps identify a measurement difference, not its cause or an automatic fairness remedy. Missing, stale, conflicting and unresolved restriction evidence is withheld. The small ASCII-email redactor intentionally leaves other identifiers untouched and is not general PII protection.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 25 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter25.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
