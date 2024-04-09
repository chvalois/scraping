{{
  config(
    materialized='incremental',
    unique_key='ad_id'
  )
}}

WITH src_ads AS (
    SELECT * FROM {{ ref("src_ads") }}
),

existing_ads AS (
    SELECT * FROM src_ads
    WHERE {{ is_incremental() }}
),

new_or_updated_ads AS (
    SELECT
        s.ad_id, 
        s.ad_url,
        s.ad_city,
        s.ad_zipcode,
        s.ad_surface,
        s.ad_nb_bedrooms,
        s.ad_nb_rooms,
        s.ad_price,
        s.ad_price_sqm,
        s.ad_date_scraped,
        s.ad_published_on,
        COALESCE(e.created_at, s.updated_at) AS created_at,
        s.updated_at
    FROM src_ads s
    LEFT JOIN existing_ads e ON s.ad_id = e.ad_id
    )

SELECT * 
FROM new_or_updated_ads
WHERE 
    NOT {{ is_incremental() }}           
    OR ad_id IS NULL