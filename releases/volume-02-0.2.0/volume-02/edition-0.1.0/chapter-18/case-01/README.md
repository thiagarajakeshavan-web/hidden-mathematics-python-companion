# V2C18-CASE01: Tokens, counts and a constructed scaling curve

Release 0.1.0, Volume 2, Chapter 18. Synthetic teaching fixture.

## What the program does

The BPE merge ranking is supplied explicitly; the lab does not learn that ranking. A tiny conditional count model uses counts [3,1,0,0] and add-one smoothing over four tokens. Its three stated evaluation targets produce a mean natural-log loss. The scaling observations were generated from a dimensionless constructed power law and are fitted after subtracting the stated loss floor.

## Interpret the result

The final merged symbol is milk</w>, probabilities are [0.5,0.25,0.125,0.125], NLL is 1.3862943611 nats and perplexity is 4. The fitted exponent is 0.5 and the constructed C=64 prediction is 1.25. This count model is not an LLM; this fit cannot estimate a real training bill.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 18 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter18.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
