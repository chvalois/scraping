WITH src_ads AS (
    SELECT * FROM {{ ref("src_ads") }}
),

WITH latest_ads AS (
    SELECT
        ad_id,
        MAX(updated_at) AS latest_updated_at
    FROM
        src_ads
    GROUP BY
        ad_id
),

duplicates AS (
    SELECT
        s.*
    FROM
        src_ads s
    LEFT JOIN
        latest_ads la
    ON
        s.id = la.id
        AND s.updated_at = la.latest_updated_at
    WHERE
        la.id IS NULL
)

DELETE FROM src_ads
USING duplicates
WHERE src_ads.id = duplicates.id
AND your_table_name.updated_at = duplicates.updated_at;