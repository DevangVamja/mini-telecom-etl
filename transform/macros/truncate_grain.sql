{% macro truncate_grain(ts_expr, grain='hour') %}
  {% set g = grain | lower %}
  {% if target.type == 'bigquery' %}
    {% if g == 'minute' %} TIMESTAMP_TRUNC({{ ts_expr }}, MINUTE)
    {% elif g == 'day' %}  TIMESTAMP_TRUNC({{ ts_expr }}, DAY)
    {% else %}              TIMESTAMP_TRUNC({{ ts_expr }}, HOUR)
    {% endif %}
  {% elif target.type == 'snowflake' %}
    {% if g in ['minute','hour','day'] %}
      DATE_TRUNC('{{ g }}', {{ ts_expr }})
    {% else %}
      DATE_TRUNC('hour', {{ ts_expr }})
    {% endif %}
  {% else %} {# postgres/redshift/etc. #}
    {% if g in ['minute','hour','day'] %}
      date_trunc('{{ g }}', {{ ts_expr }})
    {% else %}
      date_trunc('hour', {{ ts_expr }})
    {% endif %}
  {% endif %}
{% endmacro %}
