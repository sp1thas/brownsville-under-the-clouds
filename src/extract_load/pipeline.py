import dlt

from extract_load.resources.seeds import seed_locations
from extract_load.resources.tomorrow_api import add_merge_key, get_weather_forecast


def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="el_tomorrow_api",
        destination="postgres",
        dataset_name="raw",
    )

    load_info = pipeline.run(seed_locations | get_weather_forecast | add_merge_key)

    print(load_info)


if __name__ == "__main__":
    run_pipeline()
