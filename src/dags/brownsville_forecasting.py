from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from extract_load.pipeline import run_pipeline

with DAG(
    dag_id="brownsville_forecasting",
    schedule_interval=None,
    # schedule_interval="@hourly",
    start_date=datetime(2026, 2, 5),
    catchup=False,
    tags=["tomorrow"],
) as dag:

    extract_load = PythonOperator(
        task_id="extract_load",
        python_callable=run_pipeline,
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="""
            cd /opt/airflow/src/transform &&
            dbt deps &&
            dbt build --profiles-dir .
        """,
    )

    report = BashOperator(
        task_id="report",
        bash_command="""
            papermill \
                /opt/airflow/src/report/analysis.ipynb \
                /opt/airflow/data/output/analysis-{{ ts }}.ipynb
        """,
    )

    extract_load >> transform >> report
