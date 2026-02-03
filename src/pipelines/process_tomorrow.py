import dlt
import requests
import os
from dlt.sources.helpers import requests as dlt_requests

@dlt.resource(write_disposition="append")
def api_resource(execution_date=None):
    # TODO: Implement actual API extraction logic
    # This is a placeholder querying a random public API (JSONPlaceholder)
    url = "https://jsonplaceholder.typicode.com/posts"
    
    # Use API token from environment variable
    api_token = os.getenv("API_TOKEN")
    headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}
    
    # You can use execution_date for incremental loading or filtering
    print(f"Executing pipeline for date: {execution_date}")
    
    response = dlt_requests.get(url, headers=headers)
    response.raise_for_status()
    yield response.json()

def run_pipeline(credentials, execution_date=None):
    pipeline = dlt.pipeline(
        pipeline_name="ingest_tomorrow_api",
        destination=dlt.destinations.postgres(credentials=credentials),
        dataset_name="staging"
    )
    
    load_info = pipeline.run(api_resource(execution_date=execution_date))
    print(load_info)

if __name__ == "__main__":
    # For local testing, credentials should be provided
    # run_pipeline(credentials="postgresql://postgres:postgres@localhost:5432/destination_db")
    pass
