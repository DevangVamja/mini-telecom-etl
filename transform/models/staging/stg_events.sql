-- Staging view: clean column types and naming
with src as (
  select
    cast(timestamp as {{ dbt.type_timestamp() }})     as event_ts,
    cast(tower_id as {{ dbt.type_int() }})            as tower_id,
    cast(users_connected as {{ dbt.type_int() }})     as users_connected,
    cast(download_speed as {{ dbt.type_float() }})    as download_speed_mbps,
    cast(upload_speed as {{ dbt.type_float() }})      as upload_speed_mbps,
    cast(latency as {{ dbt.type_float() }})           as latency_ms,
    cast(weather as {{ dbt.type_string() }})          as weather,
    cast(congestion as {{ dbt.type_int() }})          as congestion_flag
  from {{ source('raw', 'tower_events') }}
)
select * from src
