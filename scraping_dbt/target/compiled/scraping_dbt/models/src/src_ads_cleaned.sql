WITH src_ads AS (
    SELECT * FROM "scraping_db"."public"."src_ads"
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

id_duplicates AS (
    SELECT
        s.*
    FROM
        src_ads s
    LEFT JOIN
        latest_ads la
    ON
        s.ad_id = la.ad_id
        AND s.updated_at = la.latest_updated_at
    WHERE
        la.ad_id IS NULL
)

SELECT * FROM src_ads
WHERE (ad_id, updated_at) NOT IN (
    SELECT 
        ad_id,
		updated_at
    FROM   
        id_duplicates
)