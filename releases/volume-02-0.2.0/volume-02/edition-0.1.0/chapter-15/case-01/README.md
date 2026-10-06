# V2C15-CASE01: Backpropagation you can audit

Release 0.1.0, Volume 2, Chapter 15. Synthetic teaching fixture.

## What the program does

The input has two features and one ReLU hidden unit. Parameters are ordered w0, w1, b, v, c. All gradients are evaluated at the original parameters before the simultaneous update. The binary cross-entropy uses natural logarithms and a stable softplus expression. Central differences perturb one parameter at a time by 1e-6. ReLU is nondifferentiable at zero; the code chooses a zero subgradient there, while the main fixture stays safely away from the kink.

## Interpret the result

Loss falls from 0.7339469673 to 0.6789767190 for this one example and learning rate. This is not a general training guarantee. Compare the analytical gradients with central differences, then try a much larger learning rate.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 15 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter15.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
