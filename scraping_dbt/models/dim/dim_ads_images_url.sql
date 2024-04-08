WITH src_ads AS (
    SELECT * FROM {{ ref("src_ads") }}
    )

SELECT 
    ad_id, 
    CASE WHEN ad_image_url = "None" THEN ad_image_url ELSE REPLACE(ad_image_url, "'", "") END AS ad_image_url,
FROM
    src_ads,
    UNNEST(SPLIT(REGEXP_REPLACE(ad_images_url, r'^\[|\]$', ''), ', ')) AS ad_image_url