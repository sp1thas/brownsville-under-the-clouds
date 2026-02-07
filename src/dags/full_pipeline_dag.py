from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from pipelines.etl_tomorrow_api import run_pipeline

with DAG(
    dag_id="full_pipeline_dag",
    schedule_interval="@hourly",
    start_date=datetime(2026, 2, 5),
    catchup=False,
    tags=["tomorrow"],
) as dag:

    extract_load = PythonOperator(
        task_id="dlt_extract_load",
        python_callable=run_pipeline,
    )

    transform = BashOperator(
        task_id="dbt_transform",
        bash_command="cd /opt/airflow/dbt && dbt build --profiles-dir .",
        env={
            "POSTGRES_HOST": "{{ conn.postgres_default.host }}",
            "POSTGRES_USER": "{{ conn.postgres_default.login }}",
            "POSTGRES_PASSWORD": "{{ conn.postgres_default.password }}",
            "POSTGRES_DB": "{{ conn.postgres_default.schema }}",
        },
    )

    generate_notebook = BashOperator(
        task_id="generate_analytics_notebook",
        bash_command="python /opt/airflow/scripts/generate_notebook.py",
        env={
            "EXECUTION_DATE": "{{ ds }}",
            "POSTGRES_HOST": "{{ conn.postgres_default.host }}",
            "POSTGRES_USER": "{{ conn.postgres_default.login }}",
            "POSTGRES_PASSWORD": "{{ conn.postgres_default.password }}",
            "POSTGRES_DB": "{{ conn.postgres_default.schema }}",
        },
    )

    extract_load >> transform >> generate_notebook
