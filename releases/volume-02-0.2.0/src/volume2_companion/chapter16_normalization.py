"""Forward-only BatchNorm and last-feature LayerNorm teaching mechanics.

Inputs have shape (examples, features). BatchNorm forward uses ddof=0.
Training running variance follows the PyTorch-style ddof=1 convention.
Inference accepts supplied frozen statistics and never updates them.
No autodiff, backward pass, training loop or torch dependency is included.
"""
import numpy as np
from .numerics import array
from .chapter15_optimizers import finite_scalar


def _settings(x, gamma, beta, epsilon):
    x = array(x, 2, 'examples-by-features input')
    gamma = array(gamma, 1, 'gamma')
    beta = array(beta, 1, 'beta')
    epsilon = finite_scalar(epsilon, 'epsilon')
    if gamma.shape != (x.shape[1],) or beta.shape != gamma.shape or epsilon <= 0:
        raise ValueError('one affine value per feature and positive epsilon required')
    return x, gamma, beta, epsilon


def _stats(running_mean, running_variance, feature_count):
    mu = array(running_mean, 1, 'running mean')
    var = array(running_variance, 1, 'running variance')
    if mu.shape != (feature_count,) or var.shape != mu.shape or np.any(var < 0):
        raise ValueError('matching feature dimensions and nonnegative running variance required')
    return mu, var


def _check_result(result):
    if not all(np.all(np.isfinite(v)) for v in result.values()):
        raise ValueError('normalization result is not representable')
    return result


def batch_norm_train(x, gamma, beta, epsilon, running_mean, running_variance, momentum):
    x, gamma, beta, epsilon = _settings(x, gamma, beta, epsilon)
    old_mean, old_var = _stats(running_mean, running_variance, x.shape[1])
    rho = finite_scalar(momentum, 'momentum')
    if x.shape[0] < 2 or not 0 <= rho <= 1:
        raise ValueError('at least two examples and momentum in [0,1] required')
    with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
        mean = np.mean(x, axis=0)
        variance = np.mean((x - mean) ** 2, axis=0)
        unbiased = variance * x.shape[0] / (x.shape[0] - 1)
        normalized = (x - mean) / np.sqrt(variance + epsilon)
        result = {'batch_mean': mean, 'batch_variance_biased': variance,
                  'batch_variance_unbiased': unbiased, 'normalized': normalized,
                  'output': gamma * normalized + beta,
                  'updated_running_mean': (1-rho)*old_mean + rho*mean,
                  'updated_running_variance': (1-rho)*old_var + rho*unbiased}
    return _check_result(result)


def batch_norm_infer(x, gamma, beta, epsilon, running_mean, running_variance):
    x, gamma, beta, epsilon = _settings(x, gamma, beta, epsilon)
    mean, variance = _stats(running_mean, running_variance, x.shape[1])
    with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
        normalized = (x - mean) / np.sqrt(variance + epsilon)
        result = {'mean_used': mean.copy(), 'variance_used': variance.copy(),
                  'normalized': normalized, 'output': gamma * normalized + beta}
    return _check_result(result)


def layer_norm(x, gamma, beta, epsilon):
    x, gamma, beta, epsilon = _settings(x, gamma, beta, epsilon)
    with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
        mean = np.mean(x, axis=1, keepdims=True)
        variance = np.mean((x - mean) ** 2, axis=1, keepdims=True)
        normalized = (x - mean) / np.sqrt(variance + epsilon)
        result = {'row_mean': mean, 'row_variance_biased': variance,
                  'normalized': normalized, 'output': gamma * normalized + beta}
    return _check_result(result)


def run(i):
    train_args = dict(x=i['batch'], gamma=i['gamma'], beta=i['beta'], epsilon=i['epsilon'],
                      running_mean=i['initial_running_mean'],
                      running_variance=i['initial_running_variance'], momentum=i['momentum'])
    infer_args = dict(x=i['batch'], gamma=i['gamma'], beta=i['beta'], epsilon=i['epsilon'],
                      running_mean=i['inference_running_mean'],
                      running_variance=i['inference_running_variance'])
    x = array(i['axis_comparison_batch'], 2)
    features = x.shape[1]
    return {'training': batch_norm_train(**train_args),
            'inference_frozen': batch_norm_infer(**infer_args),
            'axis_comparison': {
                'batch_norm': batch_norm_train(x, np.ones(features), np.zeros(features),
                       i['epsilon'], np.zeros(features), np.ones(features), .1),
                'layer_norm': layer_norm(x, np.ones(features), np.zeros(features), i['epsilon'])}}
