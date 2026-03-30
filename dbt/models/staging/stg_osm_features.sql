WITH source AS (
    SELECT *
    FROM `urban-analytics-osm.osm_raw.planet_features`
),

flattened AS (
    SELECT
        osm_id,
        feature_type,
        MAX(IF(t.key = 'building', t.value, NULL)) AS building,
        MAX(IF(t.key = 'building:levels', t.value, NULL)) AS building_levels,
        MAX(IF(t.key = 'amenity', t.value, NULL)) AS amenity,
        MAX(IF(t.key = 'highway', t.value, NULL)) AS highway,
        MAX(IF(t.key = 'surface', t.value, NULL)) AS surface,
        MAX(IF(t.key = 'oneway', t.value, NULL)) AS oneway,
        MAX(IF(t.key = 'addr:city', t.value, NULL)) AS city,
        MAX(IF(t.key = 'addr:country', t.value, NULL)) AS country
    FROM source,
    UNNEST(all_tags) t
    WHERE t.key IN (
        'building',
        'building:levels',
        'amenity',
        'highway',
        'surface',
        'oneway',
        'addr:city',
        'addr:country'
    )
    GROUP BY osm_id, feature_type
)

SELECT *
FROM flattened