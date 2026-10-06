# V2C22-CASE01: What was actually known at decision time

Release 0.1.0, Volume 2, Chapter 22. Synthetic teaching fixture.

## What the program does

Each price record has an event_time and an available_at time. First select the requested entity and records known by the decision cutoff. Only then deduplicate and quarantine conflicting ids, so a future conflict cannot erase historical knowledge. Finally apply event_time, TTL and the deterministic newest-record tie break. Times must include a time zone.

## Interpret the result

At 10:00, the A$10 observation has happened but is not available until 10:10, so the answer remains A$12. At 10:15 the answer is A$10. Missing and stale results are null. An already-known conflicting duplicate is quarantined. A TTL boundary is inclusive; one second beyond it is stale.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 22 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter22.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
