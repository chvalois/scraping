WITH src_ads AS (
    SELECT * FROM {{ ref("src_ads") }}
),

duplicates AS (
    SELECT
        ad_id,
        ROW_NUMBER() OVER (
            PARTITION BY ad_id, ad_price
            ORDER BY ad_published_on, updated_at DESC
        ) AS update_order,
		ad_published_on,
        updated_at,
		ad_price
	FROM
        src_ads s
),

max_updates_by_ad_id AS (
	SELECT 
		ad_id, MAX(update_order) AS nb_updates
	FROM 
		duplicates d
	GROUP BY 
		ad_id
)

SELECT d.*, m.nb_updates FROM duplicates d
LEFT JOIN max_updates_by_ad_id m ON d.ad_id = m.ad_id 
ORDER BY d.ad_id, d.update_order ASC