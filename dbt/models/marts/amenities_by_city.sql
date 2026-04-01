WITH amenities_cities AS (
    SELECT
        city,
        country
    FROM {{ ref('amenities') }}
    WHERE amenity IS NOT NULL
      AND city IS NOT NULL
      AND country IS NOT NULL
)

SELECT
    country,
    city,
    COUNT(*) AS num_amenities
FROM amenities_cities
GROUP BY country, city
ORDER BY num_amenities DESC