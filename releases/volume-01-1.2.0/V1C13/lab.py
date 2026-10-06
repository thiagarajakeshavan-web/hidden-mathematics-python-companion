"""V1C13-CASE01: clustering geometry and PCA, with training-only transforms."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from common import emit

SEED = 1313
POINTS = np.array([[0., 0.], [0., 2.], [2., 0.], [8., 8.], [8., 10.], [10., 8.]])
PCA_POINTS = np.array([[-2., -2.], [-1., -1.], [1., 1.], [2., 2.]])

def clustering_fixture():
    initial = np.array([[0., 0.], [8., 8.]])
    fitted = KMeans(n_clusters=2, init=initial, n_init=1, random_state=SEED).fit(POINTS)
    centers = fitted.cluster_centers_[np.argsort(fitted.cluster_centers_[:, 0])]
    distances = ((POINTS[:, None, :]-centers[None, :, :])**2).sum(axis=2)
    labels = np.argmin(distances, axis=1)
    return {"points": POINTS, "initial_centers": initial, "centers": centers, "canonical_labels": labels,
            "squared_distances_to_assigned_center": distances[np.arange(len(POINTS)), labels],
            "wcss": fitted.inertia_, "silhouette": silhouette_score(POINTS, labels),
            "new_point": [1., 1.], "new_point_squared_distances": np.sum((np.array([1., 1.])-centers)**2, axis=1),
            "one_cluster_wcss": np.sum((POINTS-POINTS.mean(axis=0))**2),
            "note": "Cluster identifiers are arbitrary. These geometric groups are not validated customer segments."}

def pca_fixture():
    centered = PCA_POINTS-PCA_POINTS.mean(axis=0)
    covariance = centered.T@centered/(len(PCA_POINTS)-1)
    values, vectors = np.linalg.eigh(covariance)
    order = np.argsort(values)[::-1]; values = values[order]; vectors = vectors[:, order]
    if vectors[0, 0] < 0:
        vectors[:, 0] *= -1
    scores = centered@vectors[:, :1]
    reconstruction = scores@vectors[:, :1].T+PCA_POINTS.mean(axis=0)
    library = PCA(n_components=1, svd_solver="full").fit(PCA_POINTS)
    return {"case_id": "V1C13-CASE02", "points": PCA_POINTS, "mean": PCA_POINTS.mean(axis=0), "sample_covariance_ddof1": covariance,
            "eigenvalues_descending": values, "leading_eigenvector_canonical_sign": vectors[:, 0],
            "scores_canonical_sign": scores.ravel(), "explained_variance_ratio": values/values.sum(),
            "rank_one_reconstruction": reconstruction,
            "squared_reconstruction_error": ((PCA_POINTS-reconstruction)**2).sum(),
            "sklearn_explained_variance": library.explained_variance_,
            "note": "Eigenvector sign may reverse with no change in the subspace or reconstruction. Full variance retention here follows from an exactly rank-one constructed dataset."}

def synthetic_activity(seed=SEED, n=360):
    rng = np.random.default_rng(seed)
    latent_group = rng.integers(0, 3, n)
    centers = np.array([[2., 18., 1.], [6., 55., 3.], [10., 90., 5.]])
    x = centers[latent_group]+rng.normal(size=(n, 3))*np.array([.7, 7., .8])
    # Values are abstract synthetic activity measurements, not actual prices.
    return x

def heldout_experiment():
    x = synthetic_activity()
    train, test = train_test_split(np.arange(len(x)), test_size=.25, random_state=SEED)
    scaler = StandardScaler().fit(x[train])
    z_train, z_test = scaler.transform(x[train]), scaler.transform(x[test])
    pca = PCA(n_components=2, svd_solver="full").fit(z_train)
    reconstructed = pca.inverse_transform(pca.transform(z_test))
    fitted = KMeans(n_clusters=3, n_init=10, random_state=SEED).fit(z_train)
    labels = fitted.predict(z_test)
    assigned = fitted.cluster_centers_[labels]
    baseline_center = z_train.mean(axis=0)
    return {"seed": SEED, "data": "three constructed activity clouds with unequal feature scales",
            "split_sizes": {"train": len(train), "test": len(test)},
            "split_indices": {"train": train, "test": test},
            "training_scaler_mean": scaler.mean_, "training_scaler_variance": scaler.var_,
            "scaler_n_samples_seen": int(scaler.n_samples_seen_),
            "pca_n_training_samples": pca.n_samples_, "training_explained_variance_ratio": pca.explained_variance_ratio_,
            "test_pca_mse_per_standardized_coordinate": np.mean((z_test-reconstructed)**2),
            "test_mean_squared_distance_k3": np.mean(np.sum((z_test-assigned)**2, axis=1)),
            "test_mean_squared_distance_k1": np.mean(np.sum((z_test-baseline_center)**2, axis=1)),
            "test_silhouette": silhouette_score(z_test, labels),
            "test_cluster_counts": np.bincount(labels, minlength=3),
            "note": "k=3 and two PCA components are fixed teaching choices, not selected using test data. k1 vs k3 distances alone cannot choose k; more centers usually reduce distortion. No labels or business outcomes are inferred from cluster IDs."}

def run():
    return {"case_id": "V1C13-CASE01", "data_status": "constructed and seeded synthetic data",
            "clustering_fixture": clustering_fixture(), "pca_fixture": pca_fixture(),
            "heldout_experiment": heldout_experiment()}

if __name__ == "__main__":
    emit("V1C13", run())
