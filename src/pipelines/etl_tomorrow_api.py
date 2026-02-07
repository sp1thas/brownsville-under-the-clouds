import dlt

from resources.seeds import seed_locations
from resources.tomorrow import flatten_weather_forecasts, get_weather_forecasts


def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="etl_tomorrow_api",
        destination="postgres",
        dataset_name="raw",
    )

    load_info = pipeline.run(
        seed_locations | get_weather_forecasts | flatten_weather_forecasts
    )

    print(load_info)


if __name__ == "__main__":
    run_pipeline()
