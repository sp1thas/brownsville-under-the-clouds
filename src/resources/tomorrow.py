import dlt
from dlt.sources.helpers.rest_client import RESTClient

from resources.seeds import seed_locations

tomorrow_client = RESTClient(
    base_url="https://api.tomorrow.io",
    headers={"apikey": dlt.secrets["tomorrow_api_key"]},
)


@dlt.transformer(data_from=seed_locations)
def get_weather_forecasts(location):
    yield tomorrow_client.get(
        "/v4/weather/forecast",
        params={"location": f"{location['latitude']},{location['longitude']}"},
    ).json()


@dlt.transformer(
    data_from=get_weather_forecasts,
    name="tomorrow_weather",
    write_disposition="merge",
    primary_key=["latitude", "longitude", "timeline_type", "time"],
)
def flatten_weather_forecasts(data):
    """
    Flattens the Tomorrow.io API response.
    The response contains 'timelines' with 'minutely', 'hourly', and 'daily' lists.
    Each list item contains 'time' and a 'values' dictionary.
    """
    location = data.get("location", {})
    timelines = data.get("timelines", {})

    for timeline_type, intervals in timelines.items():
        for interval in intervals:
            flattened_record = {
                "time": interval.get("time"),
                "timeline_type": timeline_type,
                **{f"{k}": v for k, v in location.items()},
                **interval.get("values", {}),
            }
            yield flattened_record
