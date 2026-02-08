import json

import dlt


@dlt.resource(
    name="locations",
    selected=False,
    write_disposition="merge",
    primary_key=["latitude", "longitude"],
)
def seed_locations():
    """
    Yields location coordinates from a local JSON file.
    """
    # Load coordinates
    with open("./data/input/coordinates.json") as f:
        for row in json.load(f):
            yield row
