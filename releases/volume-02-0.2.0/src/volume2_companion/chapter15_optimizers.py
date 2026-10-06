"""Two-step scalar optimizer mechanics; not a neural-training benchmark.

AdaGrad and uncentred RMSProp have no momentum or weight decay. Adam uses
zero-initialized moments and explicit bias correction; epsilon is OUTSIDE
all square roots. The public functions consume prescribed scalar gradients.
"""
import math
from .numerics import array


def finite_scalar(value, name):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number, not a boolean")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def trace(gradients, method, initial_parameter=0.0, learning_rate=0.1,
          epsilon=1e-8, beta1=0.9, beta2=0.9):
    """Return update/state traces; all accumulators start at zero each call."""
    if method not in ('adagrad', 'rmsprop', 'adam'):
        raise ValueError("method must be adagrad, rmsprop or adam")
    gradients = array(gradients, 1, 'gradients')
    theta = finite_scalar(initial_parameter, 'initial parameter')
    eta = finite_scalar(learning_rate, 'learning rate')
    eps = finite_scalar(epsilon, 'epsilon')
    b1 = finite_scalar(beta1, 'beta1')
    b2 = finite_scalar(beta2, 'beta2')
    if eta <= 0 or eps <= 0 or not 0 <= b1 < 1 or not 0 <= b2 < 1:
        raise ValueError("positive learning rate/epsilon and beta values in [0,1) required")
    m = v = s = 0.0
    records = []
    for t, raw_gradient in enumerate(gradients, 1):
        g = float(raw_gradient)
        squared = g * g
        if not math.isfinite(squared):
            raise ValueError("squared gradient is not representable")
        if method == 'adagrad':
            s += squared
            numerator, scale = g, s
            state = {'sum_squares': s}
        elif method == 'rmsprop':
            v = b2 * v + (1 - b2) * squared
            numerator, scale = g, v
            state = {'second_moment': v}
        else:
            m = b1 * m + (1 - b1) * g
            v = b2 * v + (1 - b2) * squared
            mhat = m / (1 - b1 ** t)
            vhat = v / (1 - b2 ** t)
            numerator, scale = mhat, vhat
            state = {'first_moment': m, 'second_moment': v,
                     'corrected_first_moment': mhat, 'corrected_second_moment': vhat}
        if not all(math.isfinite(x) for x in state.values()):
            raise ValueError("optimizer state is not representable")
        denominator = math.sqrt(scale) + eps
        update = -eta * (numerator / denominator)
        theta += update
        if not all(math.isfinite(x) for x in (denominator, update, theta)):
            raise ValueError("optimizer update is not representable")
        records.append({'step': t, 'gradient': g, **state,
                        'denominator': denominator, 'parameter_change': update,
                        'parameter': theta})
    return {'initial_parameter': finite_scalar(initial_parameter, 'initial parameter'),
            'steps': records, 'final_parameter': theta}


def run(inputs):
    return {method: trace(method=method, **inputs)
            for method in ('adagrad', 'rmsprop', 'adam')}
