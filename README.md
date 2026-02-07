# brownsville-under-the-clouds

[![preflight](https://github.com/sp1thas/brownsville-under-the-clouds/actions/workflows/preflight.yml/badge.svg)](https://github.com/sp1thas/brownsville-under-the-clouds/actions/workflows/preflight.yml)

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

## Development

### Development Environment

This project uses `uv` for fast dependency management.

1.  **Install uv**: Follow the [official guide](https://github.com/astral-sh/uv).
2.  **Create environment and install dependencies**:
    ```bash
    uv venv
    uv pip install -r requirements.txt
    ```

### Pre-commit Hooks

This project uses `pre-commit` to maintain code quality. To set it up:

1.  **Install pre-commit**:
    ```bash
    pip install pre-commit
    ```

2.  **Install the git hook scripts**:
    ```bash
    pre-commit install
    ```

3.  **Run against all files (optional)**:
    ```bash
    pre-commit run --all-files
    ```

Hooks included:
- `black` (formatting)
- `isort` (import sorting)
- `flake8` (linting)
- `sqlfluff` (SQL linting for dbt)
- `hadolint` (Dockerfile linting)
- `check-jsonschema` (Docker Compose and GitHub Workflows validation)
- `check-yaml`, `end-of-file-fixer`, `trailing-whitespace`

### CI/CD

A GitHub Workflow named `preflight` is configured to run these hooks automatically on every push and pull request to `main` or `master` branches.

## Extending the Project

- **DLT**: Modify `pipelines/api_pipeline.py` to change the API source or extraction logic.
- **DBT**: Add or modify models in `dbt/models/`.
- **Notebook**: Customize `notebooks/template.ipynb` for your analytics and visualizations.

## Implementation Details

- **DLT**: Uses `dlt` library to load data into Postgres. Credentials are retrieved from Airflow's `postgres_default` connection.
- **DBT**: Transformations are executed via `dbt build` within the Airflow `BashOperator`.
- **Airflow**: Uses SQLite as metadata DB for simplicity (in a production environment, you should use Postgres/MySQL).
- **Notebook**: Automated using `papermill` and `nbconvert`. Outputs are saved to `notebooks/output/`.
