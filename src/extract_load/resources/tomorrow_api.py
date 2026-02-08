import hashlib

import dlt
from dlt.common.utils import digest128
from dlt.sources.helpers.rest_client import RESTClient

from extract_load.resources.seeds import seed_locations

tomorrow_client = RESTClient(
    base_url="https://api.tomorrow.io",
    headers={"apikey": dlt.secrets["tomorrow_api_key"]},
)


@dlt.resource(data_from=seed_locations)
def get_weather_forecast(location):
    yield tomorrow_client.get(
        "/v4/weather/forecast",
        params={"location": f"{location['latitude']},{location['longitude']}"},
    ).json()


@dlt.transformer(
    data_from=get_weather_forecast,
    table_name="tomorrow__weather_forecasts",
    write_disposition="merge",
    primary_key="forecast_id",
    max_table_nesting=3,
)
def add_merge_key(data):
    location = data.get("location")
    for timeline_type, timeline in data.get("timelines", {}).items():
        for item in timeline:
            yield {
                "forecast_id": digest128(
                    "|".join(
                        (
                            str(location["lat"]),
                            str(location["lon"]),
                            timeline_type,
                            item["time"],
                        )
                    )
                ),
                "location": location,
                "timeline_type": timeline_type,
                **item,
            }
