# V2C16-CASE02: BatchNorm training, inference and axes

This is a forward-only normalisation lab, not a trained neural-network benchmark. Input arrays have shape (examples, features). It computes training BatchNorm, inference with explicitly supplied frozen statistics, and a separate BatchNorm-versus-LayerNorm axis comparison. Gamma and beta are supplied affine values; no backward pass or parameter learning runs.

For batch [[1],[3]], gamma=[2], beta=[0.5], epsilon=1e-5, training mean is 2 and biased forward variance is 1. Epsilon is INSIDE the square root. Outputs are approximately −1.499990 and 2.499990. The normalised variance is 1/1.00001, not exactly one.

The running update follows the PyTorch-style convention: (1−rho)*old+rho*new with rho=0.1. Only the running variance uses unbiased variance m/(m−1) times the biased batch variance. From initial running mean 0 and variance 1, the updated values are 0.2 and 1.1. Training rejects fewer than two examples because this running-variance convention requires m>1.

The inference comparison uses DIFFERENT explicitly supplied frozen mean 1 and variance 4, not the just-updated training values. Outputs are 0.5 and approximately 2.4999975. Inference never mutates the supplied statistics and accepts one example. Another request in the same inference batch does not change the first output; a training batch can change the output.

For rows [[1,3],[5,7]], BatchNorm pools rows by column: means [3,5], variances [4,4]. LayerNorm pools features within each row: means [[2],[6]], variances [[1],[1]]. With unit scale and zero shift the approximate outputs are [[−1,−1],[1,1]] versus [[−1,1],[−1,1]]. Epsilon slightly reduces these magnitudes. This LayerNorm uses the same current-input calculation at training and inference; there is no running-stat mode.

The implementation is src/volume2_companion/chapter16_normalization.py. Tests independently derive both variance conventions and affine outputs, check frozen-stat immutability and batch independence, and distinguish the normalised axes. Constant batches, a single LayerNorm feature, zero running variance, invalid dimensions, negative running variance and invalid epsilon are covered. The implementation has no convolutional spatial axes, distributed statistic synchronisation, backward differentiation or framework runtime dependency.

From the companion root:

    python run_cases.py --chapter 16 --case 2 --verify

Or run this case’s run.py from any folder. Preserve fixture.json before changes. expected.json records executed output; changing it is not independent verification. No network, downloads, API keys or credentials are used.
