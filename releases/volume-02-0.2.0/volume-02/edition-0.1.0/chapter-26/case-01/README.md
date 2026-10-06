# V2C26-CASE01: Drift, error budgets and whole-path latency

Release 0.1.0, Volume 2, Chapter 26. Synthetic teaching fixture.

## What the program does

Total variation compares aligned category distributions. Availability is computed from synthetic request counts, not wall-clock uptime. The error budget is (1-target)*requests; remaining budget may become negative. Little’s law uses a stable system and consistent arrival/service boundaries. The latency comparison adds CPU, transfer and GPU components in the same sequential path.

## Interpret the result

Total variation is 0.2. Thirty failures among 10,000 requests give availability 0.997 against a 0.995 target, leaving 20 of 50 permitted bad requests. The mean concurrency is 20 requests/second times 0.2 seconds = 4. Assumed total latency changes from 110 ms to 70 ms, a 1.5714 ratio. Drift alone does not prove degraded predictions, and no live service or GPU was timed.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 26 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter26.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
