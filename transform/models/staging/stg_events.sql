-- Staging view: clean column types and naming
with src as (
  select
    site_id,
    cast(timestamp as timestamp) as event_ts,
    event_type,
    cast(metric_value as float64) as metric_value
  from {{ source('raw','events') }}
)
select * from src
