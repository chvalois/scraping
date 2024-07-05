
  
    

  create  table "scraping_db"."public"."src_prix_m2__dbt_tmp"
  
  
    as
  
  (
    WITH raw_prix_m2 AS (
    SELECT * FROM "scraping_db"."public"."prix_m2_commune"
    )

SELECT 
    CASE 
        WHEN LENGTH(CAST(zipcode AS TEXT)) = 4 THEN CONCAT('0', CAST(zipcode AS TEXT))
        ELSE CAST(zipcode AS TEXT)
        /* WHEN LENGTH(CAST(zipcode AS STRING)) = 4 THEN CONCAT("0", CAST(zipcode AS STRING))
        ELSE CAST(zipcode AS STRING) /* For GCP */ */
        END
        AS zipcode,
    city_name,
    house_type,
    CAST(prix_m2 AS INTEGER) AS prix_m2
FROM
    raw_prix_m2
  );
  