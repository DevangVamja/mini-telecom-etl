-- Simple KPI fact table
with base as (
  select
    site_id,
    date_trunc(event_ts, minute) as minute_ts,
    max(case when event_type = 'throughput_mbps' then metric_value end) as throughput_mbps,
    max(case when event_type = 'latency_ms' then metric_value end) as latency_ms,
    max(case when event_type = 'packet_loss_pct' then metric_value end) as packet_loss_pct
  from {{ ref('stg_events') }}
  group by 1,2
)
select * from base
