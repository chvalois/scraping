# Generate a database of real estate ads

What does this project do?

![image](https://github.com/chvalois/scraping/assets/32735527/e087ee8a-3d39-494a-a55e-ec54b6cdc8aa)


1. Initiate Airflow and Postgres services through Docker-Compose

```
# Sous Windows
docker-compose -f docker-compose.windows.yaml up -d

# Sous Linux
docker-compose up -d
```

2. Airflow will scrap a website containing ads everyday at 9PM and then inject data in a PostgresDB




3. Airbyte passes data from Postgres to Big Query





4. dbt transforms data inside Big Query dataset



```
dbt run
dbt snapshot
```
