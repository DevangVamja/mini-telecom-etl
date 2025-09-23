{{ config(
    materialized='incremental',
    unique_key='tower_id_hour',
    on_schema_change='sync_all_columns'
) }}

with base as (
  select
    tower_id,
    {{ truncate_grain('event_ts', 'hour') }} as hour_ts,
    users_connected,
    download_speed_mbps,
    upload_speed_mbps,
    latency_ms,
    weather,
    congestion_flag
  from {{ ref('stg_tower_events') }}
),

-- If duplicates exist within the hour, aggregate safely
agg as (
  select
    tower_id,
    hour_ts,
    avg(users_connected)        as users_connected_avg,
    avg(download_speed_mbps)    as download_speed_avg,
    avg(upload_speed_mbps)      as upload_speed_avg,
    avg(latency_ms)             as latency_avg,
    max(congestion_flag)        as congestion_flag,   
    min(weather)                as weather_sample
  from base
  group by 1,2
),

features as (
  select
    *,
    -- avoid divide-by-zero
    (download_speed_avg + upload_speed_avg) / nullif(users_connected_avg, 0) as speed_per_user,
    case when latency_avg > 80 then 1 else 0 end as latency_sla_breach,
    case when download_speed_avg < 10 then 1 else 0 end as speed_sla_breach
  from agg
)

select
  {{ dbt_utils.generate_surrogate_key(['tower_id','hour_ts']) }} as tower_id_hour,
  *
from features

{% if is_incremental() %}
  where hour_ts > (select coalesce(max(hour_ts), '1900-01-01') from {{ this }})
{% endif %}
