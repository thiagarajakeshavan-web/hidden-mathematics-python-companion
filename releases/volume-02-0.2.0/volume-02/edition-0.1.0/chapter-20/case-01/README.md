# V2C20-CASE01: Retrieval is separate from eligibility

Release 0.1.0, Volume 2, Chapter 20. Synthetic teaching fixture.

## What the program does

The three vector coordinates are explicit lexical terms: vegan, dinner and powder. They are not learned embeddings. Unauthorized and stale records are removed before their vectors are scored. Exact cosine ranks the remaining records with deterministic id-based tie breaking. A separate restriction evidence gate is applied after retrieval, and score cannot override it.

## Interpret the result

D1 ranks first with cosine approximately 1 but is withheld for unknown restriction evidence. D2 has cosine 0.7071067812 and is a synthetic review candidate. D3 is stale and D4 belongs outside the authorized set. Review eligibility never guarantees allergen safety. Try an unauthorized record with an invalid vector: it must not be scored.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 20 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter20.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
