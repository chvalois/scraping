
      
        
            delete from "scraping_db"."public"."src_ads_cleaned_backup_incremental"
            where (
                ad_id) in (
                select (ad_id)
                from "src_ads_cleaned_backup_incremental__dbt_tmp151452139486"
            );

        
    

    insert into "scraping_db"."public"."src_ads_cleaned_backup_incremental" ("ad_id", "ad_url", "ad_city", "ad_zipcode", "ad_surface", "ad_nb_bedrooms", "ad_nb_rooms", "ad_price", "ad_price_sqm", "ad_date_scraped", "ad_published_on", "created_at", "updated_at")
    (
        select "ad_id", "ad_url", "ad_city", "ad_zipcode", "ad_surface", "ad_nb_bedrooms", "ad_nb_rooms", "ad_price", "ad_price_sqm", "ad_date_scraped", "ad_published_on", "created_at", "updated_at"
        from "src_ads_cleaned_backup_incremental__dbt_tmp151452139486"
    )
  