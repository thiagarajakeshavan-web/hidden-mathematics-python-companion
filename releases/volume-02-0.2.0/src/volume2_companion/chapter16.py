"""Forward mechanics of cross-correlation, recurrent state and an LSTM cell."""
import math
import numpy as np
from .numerics import array


def cross_correlation(signal, kernel, stride=1, padding=0):
    x, k = array(signal, 1), array(kernel, 1)
    if not isinstance(stride, int) or stride <= 0 or not isinstance(padding, int) or padding < 0:
        raise ValueError("stride must be a positive integer; padding a nonnegative integer")
    x = np.pad(x, padding)
    if len(k) > len(x):
        raise ValueError("kernel longer than padded signal")
    return np.array([x[j:j+len(k)] @ k for j in range(0, len(x)-len(k)+1, stride)])


def rnn(sequence, wx, wh, b, h0=0.0):
    sequence = array(sequence, 1)
    wx, wh, b, h = array([wx, wh, b, h0], 1)
    states = []
    for x in sequence:
        h = math.tanh(wx*x + wh*h + b)
        states.append(h)
    return np.array(states)


def lstm_cell(previous_cell, forget, input_gate, candidate, output_gate):
    values = array([previous_cell, forget, input_gate, candidate, output_gate], 1)
    if not all(0 <= v <= 1 for v in (forget, input_gate, output_gate)) or not -1 <= candidate <= 1:
        raise ValueError("sigmoid gates must be in [0,1] and tanh candidate in [-1,1]")
    cell = forget*previous_cell + input_gate*candidate
    return float(cell), float(output_gate * math.tanh(cell))


def run(i):
    conv = cross_correlation(i["signal"], i["kernel"], i["conv_stride"], i["conv_padding"])
    cell, hidden = lstm_cell(i["lstm_previous_cell"], i["lstm_forget_gate"], i["lstm_input_gate"], i["lstm_candidate"], i["lstm_output_gate"])
    return {"convolution_output": conv, "relu_output": np.maximum(conv, 0),
            "rnn_hidden_sequence": rnn(i["rnn_x"], i["rnn_wx"], i["rnn_wh"], i["rnn_b"], i["rnn_h0"]),
            "lstm_cell": cell, "lstm_hidden": hidden,
            "ten_step_carry_075": 0.75**10, "ten_step_carry_099": 0.99**10}
