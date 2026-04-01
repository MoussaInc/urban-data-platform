WITH buildings AS (
    SELECT *
    FROM {{ ref('stg_osm_features') }}
    WHERE building IS NOT NULL
      AND osm_id IS NOT NULL
)

SELECT *
FROM buildings