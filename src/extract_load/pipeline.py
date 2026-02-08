import dlt

from extract_load.resources import add_merge_key, get_weather_forecast, seed_locations


def run_pipeline():
    """
    Initializes and runs the dlt pipeline to extract weather data and load it into Postgres.
    """
    pipeline = dlt.pipeline(
        pipeline_name="el_tomorrow_api",
        destination="postgres",
        dataset_name="raw",
    )

    load_info = pipeline.run(seed_locations | get_weather_forecast | add_merge_key)

    print(load_info)


if __name__ == "__main__":
    run_pipeline()
