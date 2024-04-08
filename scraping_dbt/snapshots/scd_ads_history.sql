{% snapshot scd_ads_history %}
{{
    config(
        target_schema='DEV',
        unique_key='ad_id',
        strategy='timestamp',
        updated_at='updated_at',
        invalidate_hard_deletes=True
        )
    }}

SELECT * FROM {{ ref('src_ads_cleaned') }}
{% endsnapshot %}