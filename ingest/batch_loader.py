# Simple idempotent batch loader template.
# - Reads CSV and writes partitioned CSV files (simulated bronze layer).
# - Demonstrates dedupe logic before writing.

import pandas as pd
from pathlib import Path

def load_events(csv_path: str, out_dir: str):
    df = pd.read_csv(csv_path)
    # Idempotency: drop exact duplicates based on business key
    business_key = ["site_id", "timestamp", "event_type"]
    df = df.drop_duplicates(subset=business_key, keep="last")
    # Simulated partitioning by event_type
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for evt, sub in df.groupby("event_type"):
        sub.to_csv(out / f"{evt}.csv", index=False)
    return df

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="data/sample/events.csv")
    p.add_argument("--out", default="data/bronze")
    args = p.parse_args()
    df = load_events(args.csv, args.out)
    print(f"Wrote {len(df)} records to {args.out}")
