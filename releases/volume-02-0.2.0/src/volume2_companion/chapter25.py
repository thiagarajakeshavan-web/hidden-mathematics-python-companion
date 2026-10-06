"""A narrow mock policy gate, abstract cohort metrics and deliberately limited redaction."""
import re
from .chapter23 import confusion


def policy_reasons(request):
    # These flags must be supplied by trusted application controls in a real system.
    # This fixture tests a predicate, not identity verification or model robustness.
    reasons = []
    if request.get("action") != "read_catalogue": reasons.append("action_not_allowlisted")
    if request.get("trusted_user_authorized") is not True: reasons.append("missing_trusted_authorization")
    if request.get("role_permitted") is not True: reasons.append("role_not_permitted")
    if request.get("arguments_valid") is not True: reasons.append("invalid_arguments")
    if request.get("sensitive_export") is not False: reasons.append("sensitive_export_or_unknown_status")
    return reasons


def policy(request):
    return "deny" if policy_reasons(request) else "allow"


def cohort_metrics(counts):
    if set(counts) != {"tp", "fn", "fp", "tn"} or any(not isinstance(x, int) or isinstance(x, bool) or x < 0 for x in counts.values()):
        raise ValueError("cohort requires four nonnegative integer confusion counts")
    tp, fn, fp, tn = (counts[k] for k in ("tp", "fn", "fp", "tn"))
    total = tp+fn+fp+tn
    return {"tpr": tp/(tp+fn) if tp+fn else None, "fpr": fp/(fp+tn) if fp+tn else None,
            "accuracy": (tp+tn)/total if total else None, "size": total}


def evidence_gate(status):
    return "review_eligible" if status == "current_resolved" else "withhold"


def redact_ascii_email(text):
    # Incomplete by design: not a general PII detector, Unicode email parser or DLP system.
    return re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[EMAIL]", text)


def run(i):
    a, b = cohort_metrics(i["group_a"]), cohort_metrics(i["group_b"])
    gap = lambda name: None if a[name] is None or b[name] is None else abs(a[name]-b[name])
    return {"group_a": a, "group_b": b, "tpr_gap": gap("tpr"), "fpr_gap": gap("fpr"),
            "policy_decisions": {p["id"]: policy(p) for p in i["policy_cases"]},
            "policy_denial_reasons": {p["id"]: policy_reasons(p) for p in i["policy_cases"]},
            "restriction_evidence_decisions": {s: evidence_gate(s) for s in i["allergy_evidence"]},
            "synthetic_redaction": redact_ascii_email("Contact reader@example.test for the synthetic quote."),
            "warning": "Review eligibility is never an allergen-safety guarantee; this policy is not a prompt-injection benchmark."}
