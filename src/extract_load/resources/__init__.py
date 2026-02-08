"""
This module provides dlt resources and transformers for fetching and processing weather data.
"""

from extract_load.resources.seeds import seed_locations
from extract_load.resources.tomorrow_api import (
    add_merge_key,
    get_weather_forecast,
)

__all__ = ["seed_locations", "get_weather_forecast", "add_merge_key"]
