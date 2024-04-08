WITH raw_ads AS (
    SELECT * FROM {{ source('scraping_ads', 'ads')}}
    )

SELECT 
    RIGHT(url, 6) AS ad_id,
    url AS ad_url,
    lieu AS ad_location,
    CASE WHEN lieu = '-' THEN NULL ELSE REGEXP_EXTRACT(lieu, r'^([^(]+)') END AS ad_city,
    CASE WHEN lieu = '-' THEN NULL ELSE REGEXP_EXTRACT(lieu, r'\(([^)]+)\)') END AS ad_zipcode,
    surface AS ad_surface,
    IFNULL(nb_chambres, 0) AS ad_nb_bedrooms,
    nb_pieces AS ad_nb_rooms,
    CAST(REPLACE(price, ' ', '') AS INT64) AS ad_price,
    CAST(REPLACE(prix_m2, ' ', '') AS INT64) AS ad_price_sqm,
    tags AS ad_tags,
    tag_1 AS ad_tag_1,
    tag_2 AS ad_tag_2,
    tag_3 AS ad_tag_3,
    images_url AS ad_images_url,
    date_scraped AS ad_date_scraped,
    PARSE_DATE("%d/%m/%Y", date_publication) AS ad_published_on,
    CURRENT_TIMESTAMP() AS created_at,
    CURRENT_TIMESTAMP() AS updated_at 
FROM
    raw_ads