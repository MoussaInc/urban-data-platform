WITH buildings AS (
    SELECT country, city, COUNT(*) AS num_buildings
    FROM {{ ref('building') }}
    WHERE city IS NOT NULL AND country IS NOT NULL
    GROUP BY country, city
),

amenities AS (
    SELECT country, city, COUNT(*) AS num_amenities
    FROM {{ ref('amenities') }}
    WHERE city IS NOT NULL AND country IS NOT NULL
    GROUP BY country, city
),

roads AS (
    SELECT country, city, COUNT(*) AS num_roads
    FROM {{ ref('roads') }}
    WHERE city IS NOT NULL AND country IS NOT NULL
    GROUP BY country, city
),

combined AS (
    SELECT
        b.country,
        b.city,
        b.num_buildings,
        COALESCE(a.num_amenities, 0) AS num_amenities,
        COALESCE(r.num_roads, 0) AS num_roads
    FROM buildings b
    LEFT JOIN amenities a USING (country, city)
    LEFT JOIN roads r USING (country, city)
),

scored AS (
    SELECT *,
        -- Normalisation simple
        num_buildings / MAX(num_buildings) OVER() AS norm_buildings,
        num_amenities / MAX(num_amenities) OVER() AS norm_amenities,
        num_roads / MAX(num_roads) OVER() AS norm_roads
    FROM combined
)

SELECT
    country,
    city,
    num_buildings,
    num_amenities,
    num_roads,

    -- Score final
    (norm_buildings * 0.5 +
     norm_amenities * 0.3 +
     norm_roads * 0.2) AS urban_density_score

FROM scored
ORDER BY urban_density_score DESC
LIMIT 100