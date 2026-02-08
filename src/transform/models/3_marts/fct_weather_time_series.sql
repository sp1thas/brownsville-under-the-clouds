WITH hourly_forecast AS (
    SELECT
        lat,
        lon,
        time,
        temperature,
        humidity,
        wind_speed,
        precipitation_probability
    FROM {{ ref('stg_tomorrow__weather_forecast') }}
    WHERE timeline_type = 'hourly'
)

SELECT
    lat,
    lon,
    time,
    temperature,
    humidity,
    wind_speed,
    precipitation_probability
FROM hourly_forecast
WHERE time >= CURRENT_TIMESTAMP - INTERVAL '1 day'
  AND time <= CURRENT_TIMESTAMP + INTERVAL '5 days'
ORDER BY lat, lon, time
