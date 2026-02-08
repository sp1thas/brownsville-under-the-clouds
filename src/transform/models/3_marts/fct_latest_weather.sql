WITH latest_observations AS (
    SELECT
        lat,
        lon,
        time,
        temperature,
        wind_speed,
        ROW_NUMBER() OVER (PARTITION BY lat, lon ORDER BY time DESC) as rn
    FROM {{ ref('stg_tomorrow__weather_forecast') }}
)

SELECT
    lat,
    lon,
    time AS latest_observation_time,
    temperature AS latest_temperature,
    wind_speed AS latest_wind_speed
FROM latest_observations
WHERE rn = 1
