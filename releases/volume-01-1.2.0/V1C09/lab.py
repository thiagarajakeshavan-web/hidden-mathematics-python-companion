"""V1C09-CASE01: four learning-paradigm arithmetic demonstrations."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn.cluster import KMeans
from common import emit

def discounted_return(rewards, gamma):
    rewards = np.asarray(rewards, dtype=float)
    if rewards.ndim != 1 or rewards.size == 0 or not np.isfinite(rewards).all() or not 0 <= gamma <= 1:
        raise ValueError("Use finite nonempty one-dimensional rewards and gamma in [0,1].")
    return float(np.dot(rewards, gamma ** np.arange(len(rewards))))

def q_learning_update(q_current, learning_rate, reward, gamma, next_max_q):
    if not 0 <= learning_rate <= 1 or not 0 <= gamma <= 1:
        raise ValueError("Learning rate and discount must lie in [0,1].")
    if not np.isfinite([q_current, reward, next_max_q]).all():
        raise ValueError("Q values and reward must be finite.")
    return q_current + learning_rate * (reward + gamma * next_max_q - q_current)

def run():
    y = np.array([2., 4., 6.]); prediction = np.array([3., 4., 5.])
    x = np.array([1., 2., 8., 9.]).reshape(-1, 1)
    initial = np.array([1., 8.]).reshape(-1, 1)
    fitted = KMeans(n_clusters=2, init=initial, n_init=1, random_state=909).fit(x)
    centers = np.sort(fitted.cluster_centers_.ravel())
    labels = np.argmin((x-centers)**2, axis=1)
    return {"case_id": "V1C09-CASE01", "data_status": "constructed educational fixtures only",
        "supervised": {"y": y, "prediction": prediction,
                       "squared_errors": (prediction-y)**2, "mse": np.mean((prediction-y)**2)},
        "clustering": {"x": x.ravel(), "initial_centers": initial.ravel(),
                       "initial_inertia": np.min((x-initial.ravel())**2, axis=1).sum(),
                       "centers_after_update": centers, "labels": labels, "inertia_final": fitted.inertia_},
        "self_supervised": {"observed_token": "rice", "predicted_probability": .7,
                            "negative_log_likelihood_nats": -np.log(.7),
                            "note": "A loss calculation for a masked-token target derived from text. No language model is trained."},
        "reinforcement": {"gamma": .9, "policy_a_rewards": [5, 4], "policy_b_rewards": [7, 1],
            "policy_a_return": discounted_return([5, 4], .9), "policy_b_return": discounted_return([7, 1], .9),
            "q_current": 2., "learning_rate": .5, "reward": 1., "next_max_q": 4.,
            "q_updated": q_learning_update(2., .5, 1., .9, 4.),
            "note": "Two supplied reward sequences and one Q update, not trained policies or a live shopping experiment."},
        "scope": "Learning signals and objective arithmetic; no operational performance, purchase, health or delivery claims."}

if __name__ == "__main__":
    emit("V1C09", run())
