"""Bitemporal point-in-time selection with conservative conflict quarantine."""
from datetime import datetime, timedelta, timezone
from .numerics import positive
from .chapter21 import money


def timestamp(text):
    dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("timestamps must carry a time zone")
    return dt.astimezone(timezone.utc)


def deduplicate(records):
    unique, conflicts = {}, set()
    for r in records:
        if not isinstance(r.get("id"), str) or not r["id"]:
            raise ValueError("record needs a stable nonempty id")
        timestamp(r["event_time"]); timestamp(r["available_at"]); money(r["price_aud"])
        if r["id"] in unique and r != unique[r["id"]]:
            conflicts.add(r["id"])
        else:
            unique[r["id"]] = dict(r)
    return [r for key, r in unique.items() if key not in conflicts], sorted(conflicts)


def as_of(records, decision_time, ttl_hours, entity, default_entity=None):
    now = timestamp(decision_time)
    ttl = timedelta(hours=positive(ttl_hours, "TTL hours", allow_zero=True))
    # Historical quarantine must itself be point-in-time: an unseen future
    # conflict cannot erase a row that was known at the decision cutoff.
    known = [r for r in records if r.get("entity", default_entity) == entity
             and timestamp(r["available_at"]) <= now]
    unique, conflicts = deduplicate(known)
    eligible = [r for r in unique if timestamp(r["event_time"]) <= now
                and now - timestamp(r["event_time"]) <= ttl]
    # Explicit deterministic tie-break: event time, available time, then record id.
    eligible.sort(key=lambda r: (timestamp(r["event_time"]), timestamp(r["available_at"]), r["id"]))
    selected = eligible[-1] if eligible else None
    return {"selected_id": None if selected is None else selected["id"],
            "price_aud": None if selected is None else selected["price_aud"], "quarantined_ids": conflicts}


def run(i):
    records, entity = i["records"], i["entity"]
    select = lambda time, e=entity, rs=records: as_of(rs, time, i["ttl_hours"], e, entity)
    conflicting = records + [{**records[0], "price_aud": 99}]
    return {"at_1000": select(i["decision_time"]), "at_1015": select("2026-10-06T10:15:00Z"),
            "missing_entity": select(i["decision_time"], "missing"),
            "all_stale": select("2026-10-07T12:00:00Z"),
            "conflicting_duplicate": select(i["decision_time"], rs=conflicting),
            "unique_record_count": len(deduplicate(records)[0])}
