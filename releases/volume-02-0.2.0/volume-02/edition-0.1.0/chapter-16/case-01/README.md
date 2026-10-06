# V2C16-CASE01: Three architectural building blocks

Release 0.1.0, Volume 2, Chapter 16. Synthetic teaching fixture.

## What the program does

The CNN calculation is one-dimensional cross-correlation: the kernel is not flipped. The recurrent network uses the previous hidden state, not the previous raw input. The LSTM receives explicitly supplied gate outputs; the gates are not learned from the signal in this lab. Its cell state is f*c_previous + i*candidate and its hidden output is o*tanh(cell).

## Interpret the result

The correlation gives [-1,-2,1], the RNN states are about [0.462117,0.227033], and the LSTM cell is 0.7. The quantities 0.75^10 and 0.99^10 isolate a direct fixed-gate carry path; they are not the full recurrent gradient. Try closing the output gate while retaining the cell.

## Run and inspect

From the companion root:

    python run_cases.py --chapter 16 --verify

Or run this directory's run.py using your Python interpreter. fixture.json contains every input and its scope. expected.json contains actual recorded output, not a production promise. The algorithm is in src/volume2_companion/chapter16.py; tests/test_companion.py includes analytic, boundary and negative tests. README_TA.md explains the same case in Tamil.

Before changing a fixture, make a copy. State your assumptions, preserve units, work out a small result by hand, then run the code. Do not treat a changed expected file as proof of correctness. No network, model download, paid API or credentials are used.
