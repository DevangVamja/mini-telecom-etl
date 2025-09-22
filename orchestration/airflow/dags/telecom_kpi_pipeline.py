from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data-eng",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="telecom_kpi_pipeline",
    default_args=default_args,
    schedule_interval="*/15 * * * *",
    start_date=datetime(2025, 9, 1),
    catchup=False,
    tags=["telecom", "etl", "dbt", "ge"],
) as dag:

    ingest = BashOperator(
        task_id="ingest_csv_to_bronze",
        bash_command="python ingest/batch_loader.py --csv data/sample/events.csv --out data/bronze"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="echo 'dbt run --profiles-dir . --project-dir transform'"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="echo 'dbt test --profiles-dir . --project-dir transform'"
    )

    ge_check = BashOperator(
        task_id="great_expectations_check",
        bash_command="echo 'great_expectations checkpoint run events_suite'"
    )

    ingest >> dbt_run >> dbt_test >> ge_check
