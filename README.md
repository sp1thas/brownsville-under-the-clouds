# brownsville-under-the-clouds

[![build](https://github.com/sp1thas/brownsville-under-the-clouds/actions/workflows/build.yml/badge.svg)](https://github.com/sp1thas/brownsville-under-the-clouds/actions/workflows/build.yml)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)

This project implements an end-to-end weather forecasting pipeline for Brownsville, using DLT to fetch data from the Tomorrow.io API, dbt for transformations, and Airflow for orchestration, all running within Docker.

## Project Structure

- `src/extract_load/`: DLT pipeline scripts for data extraction and loading.
- `src/transform/`: DBT project for data transformation.
- `src/dags/`: Airflow DAGs for orchestration.
- `src/report/`: Jupyter notebooks for data analysis and reporting.
- `data/`: Local data files (input coordinates and output reports).
- `requirements/`: Python dependency files.

## Tooling

- **Postgres**: An all-around relational db which never loses.
- **DLT**: For extract and load purposes, built-in implementation for ingestion from various sources including APIs and various destinations.
- **dbt**: For data transformations, data testing, documentation etc.
- **Airflow**: A quite standard option for the orchestration of the ELT pipeline.
- **Notebooks & Reporting**: Jupyter notebooks, pandas, papermill, and matplotlib are used for data analysis and generating automated reports.

## Prerequisites

- Docker and Docker Compose installed.
- A Tomorrow.io API token (see `.env.template`).

## How to Run

1.  **Set up environment variables**:
    Copy `.env.template` to `.env` and provide your Tomorrow.io API token:
    ```bash
    cp .env.template .env
    ```
    Edit `.env` and set `TOMORROW_API_KEY`.

2.  **Start the services**:
    ```bash
    docker-compose up
    ```

3.  **Access Airflow**:
    Open `http://localhost:8080` in your browser.
    Login with: `admin` / `admin`.

4.  **Run DAGs**:
    - `brownsville_forecasting`: This runs the end-to-end pipeline (DLT API -> DBT -> Notebook).

5.  **Check Results**:
    After the DAG completes, check the generated notebook in the `data/output/` directory (e.g., `analysis-2026-02-08T16:31:12.ipynb`) to get insights and visualizations.


## Assumptions and Decisions

-   **Insert Strategy**: Data is loaded using a `merge` write disposition based on `forecast_id`. Since weather forecasts for a given location and timestamp become more accurate as time passes, we overwrite previous forecasts for the same timestamp.
-   **Airflow Setup**: The current setup is minimal and intended for demonstration purposes. For production environments, several changes should be implemented:
    -   Use a dedicated metadata database (e.g., Postgres) instead of SQLite.
    -   Switch to a more robust executor (e.g., Celery or Kubernetes) instead of the `SequentialExecutor`.
    -   Deploy dedicated workers.
-   **Security**: The `AIRFLOW__WEBSERVER__SECRET_KEY` is currently set to a static value for the demo. In production, this should be a properly managed secret.
-   **Parallelism**: API calls are currently made sequentially. For larger datasets, parallelism and concurrency patterns should be applied to improve performance.
-   **Dockerization**: A single Docker image contains all dependencies for this demo. In a production environment, this should be broken down into task-specific images to optimize performance and size.
-   **Notebook Management**: The number of generated notebooks in `data/output/` will increase with each DAG run. For production, a regular cleanup or archiving strategy should be implemented to manage storage.
