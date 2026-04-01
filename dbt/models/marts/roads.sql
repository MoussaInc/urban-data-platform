WITH roads AS (
    SELECT *
    FROM {{ ref('stg_osm_features') }}
    WHERE highway IS NOT NULL
      AND osm_id IS NOT NULL
)
SELECT *
FROM roads