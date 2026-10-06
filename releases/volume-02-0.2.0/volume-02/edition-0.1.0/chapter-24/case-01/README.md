# V2C24-CASE01: Efficiency arithmetic plus a genuinely trained tiny student

Release 0.1.0, Volume 2, Chapter 24. Synthetic teaching fixture.

## What the program does

Symmetric int8 quantization uses max(abs(weights))/127 and ties-to-even rounding. Magnitude pruning produces both a keep mask and zeroed weights. Distillation trains only three categorical logits for 20 steps at learning rate 0.5 and temperature 1. Stable log-softmax computes the objective; an independent central-difference check audits its gradient.

## Interpret the result

Quantization maximum error is 0.0039370079. The student KL falls from 0.0227302548 to about 0.0002191048. The hypothetical KV cache is 50,331,648 bytes, exactly 48 MiB. Weight storage excludes activations and most runtime overhead. No GPU speed, sparse-kernel speed or full LLM compression is measured.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 24 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter24.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
