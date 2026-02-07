import os
from datetime import datetime

import papermill as pm

# Path configuration
TEMPLATE_PATH = "/opt/airflow/notebooks/template.ipynb"
OUTPUT_DIR = "/opt/airflow/notebooks/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

execution_date = os.getenv("EXECUTION_DATE", datetime.now().strftime("%Y-%m-%d"))
output_ipynb = os.path.join(OUTPUT_DIR, f"report_{execution_date}.ipynb")
output_html = os.path.join(OUTPUT_DIR, f"report_{execution_date}.html")

# Run the notebook with parameters
pm.execute_notebook(
    TEMPLATE_PATH,
    output_ipynb,
    parameters=dict(
        execution_date=execution_date,
        postgres_host=os.getenv("POSTGRES_HOST"),
        postgres_user=os.getenv("POSTGRES_USER"),
        postgres_password=os.getenv("POSTGRES_PASSWORD"),
        postgres_db=os.getenv("POSTGRES_DB"),
    ),
)

# Convert to HTML
os.system(f"jupyter nbconvert --to html {output_ipynb}")

print(f"Notebook generated: {output_ipynb} and {output_html}")
