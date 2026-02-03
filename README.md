# Minimal Data Pipeline Project

This project implements a structured data pipeline using DLT, DBT, Airflow, and Postgres, all running in Docker.

## Project Structure

- `pipelines/`: DLT pipeline scripts for data extraction.
- `dbt/`: DBT project for data transformation.
- `airflow/dags/`: Airflow DAGs for orchestration.
- `notebooks/`: Jupyter notebook templates and outputs.
- `scripts/`: Helper scripts (e.g., notebook generation).
- `data/`: Local static data files.

## Prerequisites

- Docker and Docker Compose installed.

## How to Run

1.  **Start the services**:
    ```bash
    docker-compose up -d
    ```

2.  **Access Airflow**:
    Open `http://localhost:8080` in your browser.
    Login with: `admin` / `admin`.

3.  **Run DAGs**:
    - `load_local_json_dag`: Manually trigger this to load `data/sample.json` into Postgres.
    - `full_pipeline_dag`: This runs the end-to-end pipeline (DLT API -> DBT -> Notebook).

## Extending the Project

- **DLT**: Modify `pipelines/api_pipeline.py` to change the API source or extraction logic.
- **DBT**: Add or modify models in `dbt/models/`.
- **Notebook**: Customize `notebooks/template.ipynb` for your analytics and visualizations.

## Implementation Details

- **DLT**: Uses `dlt` library to load data into Postgres. Credentials are retrieved from Airflow's `postgres_default` connection.
- **DBT**: Transformations are executed via `dbt build` within the Airflow `BashOperator`.
- **Airflow**: Uses SQLite as metadata DB for simplicity (in a production environment, you should use Postgres/MySQL).
- **Notebook**: Automated using `papermill` and `nbconvert`. Outputs are saved to `notebooks/output/`.
