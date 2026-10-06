"""Exact lexical cosine retrieval with authorization and freshness before scoring."""
import numpy as np
from .numerics import array


def cosine(query, document):
    q, d = array(query, 1, "query"), array(document, 1, "document")
    if q.shape != d.shape:
        raise ValueError("query and document dimensions must match")
    qscale, dscale = np.max(np.abs(q)), np.max(np.abs(d))
    if qscale == 0 or dscale == 0:
        raise ValueError("cosine undefined for a zero vector")
    # Scaling before norms/dot products avoids finite-input overflow/underflow.
    q, d = q/qscale, d/dscale
    return float(np.clip((q @ d) / (np.linalg.norm(q)*np.linalg.norm(d)), -1, 1))


def retrieve(query, documents):
    q = array(query, 1, "query")
    if np.max(np.abs(q)) == 0:
        raise ValueError("empty-information query needs clarification")
    ranked = []
    for doc in documents:
        # Strict booleans. Strings such as 'false' must never grant access.
        if doc.get("authorized") is not True or doc.get("current") is not True:
            continue
        ranked.append({"id": doc["id"], "score": cosine(q, doc["vector"]),
                       "restriction_review_eligible": doc.get("restriction_evidence") == "eligible_synthetic"})
    return sorted(ranked, key=lambda row: (-row["score"], row["id"]))


def run(i):
    ranked = retrieve(i["query"], i["documents"])
    return {"ranked_authorized_current": ranked,
            "restriction_review_candidate_ids": [r["id"] for r in ranked if r["restriction_review_eligible"]],
            "withheld_for_unknown_restriction_ids": [r["id"] for r in ranked if not r["restriction_review_eligible"]],
            "scope": "Lexical cosine; review eligibility is not an allergen-safety guarantee."}
