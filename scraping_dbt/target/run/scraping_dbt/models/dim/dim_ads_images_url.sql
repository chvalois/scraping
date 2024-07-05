
  
    

  create  table "scraping_db"."public"."dim_ads_images_url__dbt_tmp"
  
  
    as
  
  (
    WITH src_ads AS (
    SELECT * FROM "scraping_db"."public"."src_ads"
    )

SELECT 
    ad_id, 
    CASE WHEN ad_image_url = 'None' THEN ad_image_url ELSE REPLACE(ad_image_url, CHR(39), '') END AS ad_image_url    /* CHR(39) is ' */
FROM
    src_ads,
    UNNEST(STRING_TO_ARRAY(REGEXP_REPLACE(ad_images_url, '^\[|\]$', ''), ', ')) AS ad_image_url
    /* UNNEST(SPLIT(REGEXP_REPLACE(ad_images_url, r'^\[|\]$', ''), ', ')) AS ad_image_url /* For GCP */ */
  );
  