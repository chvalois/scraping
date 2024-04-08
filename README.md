# Generate a database of real estate ads

What does this project do?

1. Initiate Airflow and Postgres services
2. Scrap a website containing ads everyday
3. Data scraped is injected in a Postgres DB
4. Airbyte passes data from Postgres to Big Query
5. dbt transforms data inside Big Query dataset
