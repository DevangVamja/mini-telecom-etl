import pandas as pd

def idempotent_merge(existing: pd.DataFrame,
                     new: pd.DataFrame,
                     key_cols=("tower_id", "timestamp")) -> pd.DataFrame:
    """
    Idempotent merge for wide fact rows.
    - Keys: ('tower_id','timestamp') by default
    - On duplicate keys, NEW rows overwrite EXISTING rows (last write wins)
    """
    # Ensure consistent dtypes on keys
    for k in key_cols:
        if k in existing.columns and k in new.columns:
            # simple alignment; customize as needed (e.g., to_datetime for timestamp)
            if k == "timestamp":
                existing[k] = pd.to_datetime(existing[k])
                new[k] = pd.to_datetime(new[k])
            else:
                existing[k] = existing[k].astype(new[k].dtype)

    # Tag sources to control priority: existing=0, new=1 → keep last
    existing = existing.copy()
    new = new.copy()
    existing["_src_order"] = 0
    new["_src_order"] = 1

    combined = pd.concat([existing, new], ignore_index=True, sort=False)

    # Sort by keys then src_order so that new rows come last for the same key
    sort_cols = list(key_cols) + ["_src_order"]
    combined = combined.sort_values(sort_cols)

    # Drop duplicates by key, keeping the last (i.e., NEW if key duplicates)
    deduped = combined.drop_duplicates(subset=list(key_cols), keep="last").drop(columns=["_src_order"])

    # Optional: sort final output for readability
    return deduped.sort_values(list(key_cols)).reset_index(drop=True)


def test_idempotent_merge():
    # existing hourly facts for tower 1 @ 00:00 and 01:00
    existing = pd.DataFrame({
        "timestamp": ["2025-01-01 00:00:00","2025-01-01 01:00:00"],
        "tower_id": [1, 1],
        "users_connected": [150, 300],
        "download_speed": [80.0, 25.0],
        "upload_speed": [10.0, 8.0],
        "latency": [70.0, 120.0],
        "weather": ["Clear", "Clear"],
        "congestion": [0, 1],
    })

    # new has:
    # - an UPDATE for the same key (1, 00:00) with changed values
    # - a NEW key (1, 02:00)
    new = pd.DataFrame({
        "timestamp": ["2025-01-01 00:00:00","2025-01-01 02:00:00"],
        "tower_id": [1, 1],
        "users_connected": [175, 420],      # updated at 00:00, new for 02:00
        "download_speed": [60.0, 55.0],
        "upload_speed": [12.0, 9.0],
        "latency": [90.0, 65.0],
        "weather": ["Snow", "Clear"],
        "congestion": [1, 0],
    })

    out = idempotent_merge(existing, new, key_cols=("tower_id","timestamp"))

    # Convert ts to datetime for robust comparisons
    out_ts = pd.to_datetime(out["timestamp"])
    # Row for (tower_id=1, timestamp=00:00) must reflect NEW values
    row = out[(out["tower_id"] == 1) & (out_ts == pd.to_datetime("2025-01-01 00:00:00"))].iloc[0]

    assert int(row["users_connected"]) == 175
    assert float(row["download_speed"]) == 60.0
    assert float(row["upload_speed"]) == 12.0
    assert float(row["latency"]) == 90.0
    assert row["weather"] == "Snow"
    assert int(row["congestion"]) == 1

    # We should have 3 unique rows: 00:00 (updated), 01:00 (unchanged), 02:00 (new)
    assert len(out) == 3
