# V2C21-CASE01: Bounded mock tools and an authority boundary

Release 0.1.0, Volume 2, Chapter 21. Synthetic teaching fixture.

## What the program does

This deterministic workflow calls three real Python mock handlers: read_catalogue, read_labels and calculate_total. It stores catalogue text only as data. Trusted workflow code chooses every tool, and a call counter enforces the limit. No write or purchase handler exists. Calculating a total directly without validated catalogue context is denied.

## Interpret the result

A$31.50 in synthetic items plus A$5.00 delivery gives an A$36.50 quote for human review. Unknown cross-contact evidence blocks after two calls. An attempted purchase is denied without a tool call. A two-call budget ends before total calculation. This is neither an LLM agent benchmark nor a running multi-agent service.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 21 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter21.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
