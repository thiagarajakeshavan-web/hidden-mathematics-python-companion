# V2C19-CASE01: SFT, reference-corrected DPO and additive LoRA

Release 0.1.0, Volume 2, Chapter 19. Synthetic teaching fixture.

## What the program does

The SFT example trains two candidate logits with one softmax cross-entropy step. DPO compares the chosen/rejected log-probability difference with the reference policy difference. The finite-difference audit concerns partial derivatives with respect to log-probability coordinates. LoRA computes W*x + scale*B*A*x; the base matrix is retained.

## Interpret the result

The SFT preferred probability becomes 0.5498339973. The DPO loss is 0.4557463944. LoRA changes [4,10] to [4.1,10.2]. Here the adapter has four entries and the base has four entries, so this miniature example makes no parameter-saving claim. No RLHF loop or production language model is trained.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 19 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter19.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
