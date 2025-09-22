# Mini Telecom ETL: Airflow → dbt → Great Expectations (+OpenLineage)

A production-style **mini ETL** you can showcase publicly. It demonstrates:
- **Batch ingest** of telecom KPIs (CSV → bronze).
- **Orchestration** with Airflow (idempotent loads, retries, SLAs).
- **Transformations** with dbt (staging + marts, tests).
- **Data quality** with Great Expectations (freshness, nulls, ranges).
- **Lineage** with OpenLineage (YAML config).
- **Infra-as-code** (Terraform snippet for an S3 landing bucket).
- **Idempotent merge** pattern + simple integration test.

> Use this as a template to discuss SLAs, data contracts, and backfills in interviews.

## Architecture (Mermaid)

```mermaid
flowchart LR
    A[Vendor Files (CSV)] -->|ingest| B[Bronze (S3/landing)]
    B -->|Airflow DAG| C[dbt Staging Models]
    C --> D[dbt Mart Models]
    D --> E[Analytics/BI (BigQuery/Snowflake/Parquet)]
    C -->|GE checks| F[Great Expectations]
    subgraph Observability
      F -->|alerts| G[Slack/Email]
    end
    A -->|OpenLineage| H[Lineage Metadata]
    B -->|OpenLineage| H
    C -->|OpenLineage| H
    D -->|OpenLineage| H
```

## Quickstart (local demo)

1. **Explore data**: `data/sample/events.csv`  
2. **Run transform locally** (no dbt install needed to read SQL): open `transform/models/*` to inspect logic.  
3. **Airflow DAG**: `orchestration/airflow/dags/telecom_kpi_pipeline.py` (uses BashOperator placeholders for dbt/GE).  
4. **Quality**: Expectation suite under `observability/great_expectations/expectations/`.  
5. **Lineage**: `observability/lineage/openlineage.yml` (example config).  
6. **Infra**: Terraform snippet in `infra/terraform/main.tf`.  
7. **Tests**: `tests/integration/test_idempotent_merge.py` demonstrates an UPSERT pattern.

> You can swap S3/BigQuery/Snowflake as needed—this is cloud-agnostic by design.

## Talking points (copy to resume/JD tailoring)
- Built idempotent ETL with Airflow→dbt; **99.7% on-time SLAs**, freshness **<20 min** (example targets).
- Enforced data contracts with Great Expectations and column tests in dbt.
- Documented lineage with OpenLineage; added alerts on freshness and null-rate drift.
- Cut compute cost via partitioning + clustering; safe **backfills** over 12 months.

## Repo layout

```
mini-telecom-etl/
├─ data/sample/events.csv
├─ ingest/batch_loader.py
├─ orchestration/airflow/dags/telecom_kpi_pipeline.py
├─ transform/dbt_project.yml
├─ transform/models/staging/stg_events.sql
├─ transform/models/staging/schema.yml
├─ transform/models/marts/kpi/dim_sites.sql
├─ transform/models/marts/kpi/fct_network_kpi.sql
├─ observability/great_expectations/expectations/events_suite.json
├─ observability/lineage/openlineage.yml
├─ infra/terraform/main.tf
├─ tests/integration/test_idempotent_merge.py
└─ README.md
```

## Notes
- Airflow/dbt/GE commands are placeholders so the project is light-weight. Replace the `echo` commands with real CLI invocations in your environment.
- Add a scheduler (docker-compose) if you want to run it end-to-end.
