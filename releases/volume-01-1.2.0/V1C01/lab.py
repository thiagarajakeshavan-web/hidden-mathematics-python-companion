"""V1C01-CASE01: vectors, linear systems, eigendecomposition, SVD and PCA."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from common import emit

QUERY = np.array([3.0, 4.0])
PCA_DATA = np.array([[2., 1.], [2., -1.], [-2., 1.], [-2., -1.]])

def cosine(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if a.ndim != 1 or a.shape != b.shape or not np.all(np.isfinite([a, b])):
        raise ValueError("Expected finite vectors of equal length.")
    denominator = np.linalg.norm(a) * np.linalg.norm(b)
    if denominator == 0:
        raise ValueError("Cosine is undefined for a zero vector; choose an explicit business fallback.")
    return float(np.clip(np.dot(a, b) / denominator, -1., 1.))

def pca(data):
    data = np.asarray(data, dtype=float)
    centered = data - data.mean(axis=0)
    u, singular_values, vt = np.linalg.svd(centered, full_matrices=False)
    covariance = centered.T @ centered / (len(data) - 1)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    reconstructed = (u[:, :1] * singular_values[:1]) @ vt[:1]
    return {"means": data.mean(axis=0), "centered": centered, "covariance": covariance,
            "eigenvalues_descending": eigenvalues[::-1], "singular_values": singular_values,
            "explained_variance_ratio": singular_values ** 2 / np.sum(singular_values ** 2),
            "rank_one_reconstruction": reconstructed + data.mean(axis=0),
            "rank_one_squared_error": float(np.sum((centered - reconstructed) ** 2)),
            "svd_reconstruction_max_error": float(np.max(np.abs(centered - (u * singular_values) @ vt))),
            "covariance_reconstruction_max_error": float(np.max(np.abs(covariance - eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T)))}

def run():
    matrix = np.array([[2., 1.], [1., 2.]])
    rhs = np.array([8., 7.])
    solution = np.linalg.solve(matrix, rhs)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    return {"chapter": "V1C01", "case_id": "V1C01-CASE01", "synthetic": True,
            "query": QUERY, "query_norm": float(np.linalg.norm(QUERY)),
            "similarities": [{"candidate": name, "vector": vector, "dot_product": float(QUERY @ vector), "cosine": cosine(QUERY, vector)}
                             for name, vector in [("a", [4., 3.]), ("b", [-3., -4.]), ("c", [4., -3.])]],
            "zero_vector_policy": "Raise ValueError; no fabricated cosine score.",
            "linear_system": {"A": matrix, "b": rhs, "solution": solution, "residual_norm": float(np.linalg.norm(matrix @ solution - rhs)),
                              "eigenvalues": eigenvalues, "eigen_equation_max_error": float(np.max(np.abs(matrix @ eigenvectors - eigenvectors * eigenvalues)))},
            "singular_matrix_rank": int(np.linalg.matrix_rank([[1., 1.], [2., 2.]])),
            "batch_cosines": (np.array([[4.,3.],[-3.,-4.],[4.,-3.]]) @ QUERY) / (np.linalg.norm(np.array([[4.,3.],[-3.,-4.],[4.,-3.]]),axis=1) * np.linalg.norm(QUERY)),
            "pca_input": PCA_DATA, "pca": pca(PCA_DATA),
            "tensor_example_shape": list(np.zeros((2, 3, 4)).shape)}

if __name__ == "__main__":
    emit("V1C01", run())
