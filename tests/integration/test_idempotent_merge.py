import pandas as pd

def idempotent_merge(existing: pd.DataFrame, new: pd.DataFrame, key_cols):
    combined = pd.concat([existing, new], ignore_index=True)
    deduped = combined.drop_duplicates(subset=key_cols, keep="last")
    return deduped.sort_values(key_cols).reset_index(drop=True)

def test_idempotent_merge():
    existing = pd.DataFrame({
        "site_id": ["DFW001","DFW001"],
        "timestamp": ["2025-09-01T00:00:00Z","2025-09-01T00:05:00Z"],
        "event_type": ["throughput_mbps","latency_ms"],
        "metric_value": [100,30]
    })
    new = pd.DataFrame({
        "site_id": ["DFW001","DFW001"],
        "timestamp": ["2025-09-01T00:00:00Z","2025-09-01T00:10:00Z"],
        "event_type": ["throughput_mbps","packet_loss_pct"],
        "metric_value": [120,0.1]
    })
    out = idempotent_merge(existing, new, ["site_id","timestamp","event_type"])
    row = out[(out.site_id=="DFW001") & (out.timestamp=="2025-09-01T00:00:00Z") & (out.event_type=="throughput_mbps")]
    assert float(row.metric_value.values[0]) == 120.0
    assert len(out) == 3
