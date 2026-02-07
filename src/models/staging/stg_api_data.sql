-- TODO: Implement staging transformation
-- This is a placeholder model for staging raw API data
SELECT
    *
FROM {{ source('raw_api_data', 'api_resource') }}
