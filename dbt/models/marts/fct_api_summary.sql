-- TODO: Implement fact model
-- This is a placeholder model for summarized API data
SELECT
    count(*) as total_records,
    now() as processed_at
FROM {{ ref('stg_api_data') }}
