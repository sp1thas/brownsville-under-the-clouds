from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from datetime import datetime
import sys
import os

# Add dlt folder to path
sys.path.append("/opt/airflow")
from dlt.local_json_pipeline import run_local_json_pipeline

def run_dlt_json_task():
    # Retrieve connection from Airflow
    conn = BaseHook.get_connection("postgres_default")
    credentials = f"postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}"
    
    file_path = "/opt/airflow/data/sample.json"
    run_local_json_pipeline(credentials, file_path)

with DAG(
    dag_id="load_local_json_dag",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["dlt", "json"],
) as dag:

    load_json = PythonOperator(
        task_id="load_json_to_postgres",
        python_callable=run_dlt_json_task,
    )
