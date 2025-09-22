-- Tiny dimension to demonstrate marts
select distinct
  site_id,
  'Dallas-Fort Worth' as metro_area
from {{ ref('stg_events') }}
