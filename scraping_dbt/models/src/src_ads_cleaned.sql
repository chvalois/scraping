WITH src_ads AS (
    SELECT * FROM {{ ref("src_ads") }}
),

latest_ads AS (
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

SELECT * FROM src_ads
WHERE (id, updated_at) NOT IN (
    SELECT 
        la.id,
        la.latest_updated_at
    FROM   
        latest_ads la
)