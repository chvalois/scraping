
  
    

  create  table "scraping_db"."public"."dim_ads_details__dbt_tmp"
  
  
    as
  
  (
    WITH src_ads_cleaned AS (
    SELECT * FROM "scraping_db"."public"."src_ads_cleaned"
)

SELECT 
    ad_id,
    ad_url,
    ad_city,
    ad_zipcode,
    ad_nb_bedrooms,
    ad_nb_rooms,
    ad_date_scraped AS ad_last_date_scraped,
    ad_published_on AS ad_last_published_on,
    created_at,
    updated_at
FROM
    src_ads_cleaned
  );
  