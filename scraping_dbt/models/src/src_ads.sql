WITH raw_ads AS (
    SELECT * FROM {{ source('scraping_db', 'ads') }}
    )

SELECT 
    RIGHT(url, 6) AS ad_id,
    url AS ad_url,
    lieu AS ad_location,
    /* CASE WHEN lieu = '-' THEN NULL ELSE REGEXP_SUBSTR(lieu, '^([^(]+)') END AS ad_city, /* Old Method */ */
    /* CASE WHEN lieu = '-' THEN NULL ELSE REGEXP_SUBSTR(lieu, '\(([^)]+)\)') END AS ad_zipcode, /* Old Method */ */
    /* CASE WHEN lieu = '-' THEN NULL ELSE REGEXP_EXTRACT(lieu, r'^([^(]+)') END AS ad_city, /* For GCP */ */
    /* CASE WHEN lieu = '-' THEN NULL ELSE REGEXP_EXTRACT(lieu, r'\(([^)]+)\)') END AS ad_zipcode, /* For GCP */ */
    INITCAP(SPLIT_PART(url, '-', -3)) AS ad_city,
    SPLIT_PART(url, '-', -2) AS ad_zipcode,
    surface AS ad_surface,
    COALESCE(nb_chambres, 0) AS ad_nb_bedrooms,
    /* IFNULL(nb_chambres, 0) AS ad_nb_bedrooms, /* For GCP */ */
    nb_pieces AS ad_nb_rooms,
    CAST(REPLACE(price, ' ', '') AS INTEGER) AS ad_price,
    CAST(REPLACE(prix_m2, ' ', '') AS INTEGER) AS ad_price_sqm,
    /* CAST(REPLACE(price, ' ', '') AS INT64) AS ad_price, /* For GCP */ */
    /* CAST(REPLACE(prix_m2, ' ', '') AS INT64) AS ad_price_sqm, /* For GCP */ */
    tags AS ad_tags,
    tag_1 AS ad_tag_1,
    tag_2 AS ad_tag_2,
    tag_3 AS ad_tag_3,
    images_url AS ad_images_url,
    date_scraped AS ad_date_scraped,
    TO_DATE(date_publication, 'DD/mm/YYYY') AS ad_published_on,
    /* PARSE_DATE("%d/%m/%Y", date_publication) AS ad_published_on, /* For GCP */ */
    CURRENT_TIMESTAMP AS created_at,
    CURRENT_TIMESTAMP AS updated_at 
    /* CURRENT_TIMESTAMP() AS created_at,  /* For GCP */ */
    /* CURRENT_TIMESTAMP() AS updated_at  /* For GCP */ */
FROM
    raw_ads