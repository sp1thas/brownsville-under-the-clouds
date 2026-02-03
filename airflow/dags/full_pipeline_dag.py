from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.hooks.base import BaseHook
from datetime import datetime, timedelta
import sys
import os

# Add dlt folder to path
sys.path.append("/opt/airflow")
from dlt.api_pipeline import run_pipeline

def run_dlt_api_task(ds, **kwargs):
    # Retrieve connection from Airflow
    conn = BaseHook.get_connection("postgres_default")
    credentials = f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
    
    run_pipeline(credentials, execution_date=ds)

with DAG(
    dag_id="full_pipeline_dag",
    schedule_interval="@daily",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["full_pipeline"],
) as dag:

    extract_load = PythonOperator(
        task_id="dlt_extract_load",
        python_callable=run_dlt_api_task,
    )

    transform = BashOperator(
        task_id="dbt_transform",
        bash_command="cd /opt/airflow/dbt && dbt build --profiles-dir .",
        env={
            "POSTGRES_HOST": "{{ conn.postgres_default.host }}",
            "POSTGRES_USER": "{{ conn.postgres_default.login }}",
            "POSTGRES_PASSWORD": "{{ conn.postgres_default.password }}",
            "POSTGRES_DB": "{{ conn.postgres_default.schema }}",
        }
    )

    generate_notebook = BashOperator(
        task_id="generate_analytics_notebook",
        bash_command="python /opt/airflow/scripts/generate_notebook.py",
        env={
            "EXECUTION_DATE": "{{ ds }}",
            "POSTGRES_HOST": "postgres",
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
            "POSTGRES_DB": "destination_db",
        }
    )

    extract_load >> transform >> generate_notebook
