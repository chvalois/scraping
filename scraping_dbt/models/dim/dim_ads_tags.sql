WITH 
src_ads AS (
    SELECT * FROM {{ ref("src_ads") }}
    ),

temp_tags AS (
SELECT DISTINCT
    ad_id, 
    CASE WHEN ad_tag = "None" THEN ad_tag ELSE REPLACE(ad_tag, "'", "") END AS ad_tag
FROM
    src_ads,
    UNNEST(SPLIT(REGEXP_REPLACE(ad_tags, r'^\[|\]$', ''), ', ')) AS ad_tag
WHERE 
    ad_tag != "None" AND ad_tag != " "

UNION ALL
SELECT ad_id, ad_tag_1 AS ad_tag FROM src_ads WHERE ad_tag_1 IS NOT NULL AND ad_tag_1 != "None"

UNION ALL
SELECT ad_id, ad_tag_2 AS ad_tag FROM src_ads WHERE ad_tag_2 IS NOT NULL AND ad_tag_2 != "None"

UNION ALL
SELECT ad_id, ad_tag_3 AS ad_tag FROM src_ads WHERE ad_tag_3 IS NOT NULL AND ad_tag_3 != "None"
)

SELECT DISTINCT 
    ad_id, 
    ad_tag
FROM
    temp_tags
ORDER BY 
    ad_id, 
    ad_tag
