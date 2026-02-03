FROM apache/airflow:2.7.1

USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install DLT, DBT (Postgres adapter), and Jupyter related tools
RUN pip install --no-cache-dir \
    dlt[postgres] \
    dbt-postgres \
    papermill \
    nbconvert \
    pandas \
    sqlalchemy \
    psycopg2-binary \
    matplotlib \
    seaborn \
    ipykernel
