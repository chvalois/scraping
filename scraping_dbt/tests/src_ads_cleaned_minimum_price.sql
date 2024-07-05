SELECT * FROM {{ ref('src_ads_cleaned') }}
WHERE ad_price < 1000
LIMIT 10