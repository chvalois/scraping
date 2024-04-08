WITH raw_prix_m2 AS (
    SELECT * FROM {{ source('scraping_ads', 'prix_m2_commune')}}
    )

SELECT 
    CASE 
        WHEN LENGTH(CAST(zipcode AS STRING)) = 4 THEN CONCAT("0", CAST(zipcode AS STRING))
        ELSE CAST(zipcode AS STRING)
        END
        AS zipcode,
    city_name,
    house_type,
    CAST(prix_m2 AS INTEGER) AS prix_m2
FROM
    raw_prix_m2