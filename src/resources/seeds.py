import json

import dlt


@dlt.resource(
    name="locations",
    selected=False,
    write_disposition="merge",
    primary_key=["latitude", "longitude"],
)
def seed_locations():
    # Load coordinates
    with open("/opt/airflow/data/coordinates.json") as f:
        for row in json.load(f):
            yield row
