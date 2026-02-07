FROM apache/airflow:2.9.3-python3.11

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

ADD src/requirements/base.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
