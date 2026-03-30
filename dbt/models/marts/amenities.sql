WITH amenities AS (
    SELECT *
    FROM {{ ref('stg_osm_features') }}
    WHERE amenity IS NOT NULL
)
SELECT *
FROM amenities