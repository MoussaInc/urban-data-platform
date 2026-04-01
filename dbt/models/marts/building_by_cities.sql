WITH building_cities AS (
    SELECT
        city,
        country
    FROM {{ ref('building') }}
    WHERE building IS NOT NULL
      AND city IS NOT NULL
      AND country IS NOT NULL
)

SELECT
    country,
    city,
    COUNT(*) AS num_buildings
FROM building_cities
GROUP BY country, city
ORDER BY num_buildings DESC