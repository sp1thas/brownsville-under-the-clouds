import dlt
import json
import os

@dlt.resource(write_disposition="replace")
def json_resource(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    yield data

def run_local_json_pipeline(credentials, file_path):
    pipeline = dlt.pipeline(
        pipeline_name="load_coordinates",
        destination=dlt.destinations.postgres(credentials=credentials),
        dataset_name="staging"
    )
    
    load_info = pipeline.run(json_resource(file_path))
    print(load_info)

if __name__ == "__main__":
    pass
