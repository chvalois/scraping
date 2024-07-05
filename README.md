# Generate a database of real estate ads

![image](https://github.com/chvalois/scraping/assets/32735527/d16af1eb-3ca4-4ecf-be38-9112ce504135)


## Where do I start?

### 1. Initiate Airflow and Postgres services through Docker-Compose

```
# Sous Windows
docker-compose -f docker-compose.windows.yaml up -d

# Sous Linux
docker-compose -f docker-compose.linux.yaml up -d
```

### 2. Connect to the database "scraping_db" and create the table "ads"

```
docker container exec -it airflow_scheduler psql -h postgres-db -U chvalois -d scraping_db -f files/project_init_sql.pgsql
docker container exec -it airflow_scheduler psql -h postgres-db -U chvalois -f files/metabase_init_sql.pgsql

```

cd scraping_dbt
dbt seed # to add seeds to database
ALTER TABLE src_ads_cleaned REPLICA IDENTITY FULL;

dbt seed --profiles-dir /opt/airflow/dbt_profiles
dbt run --profiles-dir /opt/airflow/dbt_profiles


### 3. Create a dataset in Google Big Query

### 4. Setup Airbyte source and destination

You need to install Airbyte on your computer or on a server : 
https://docs.airbyte.com/category/deploy-airbyte

Source : PostgreSQL

Destination : Big Query

And create a synchronization every day at 9PM

## Data Flow

### 1. Airflow will scrap a website containing ads everyday at 6PM UTC and then inject data in a PostgresDB
 
### 2. Airbyte passes data from Postgres to Big Query every day at 9PM UTC

### 3. dbt transforms data inside Big Query dataset

```
dbt run
dbt snapshot
```

![2024 04 09 - 6942 - 1615x372](https://github.com/chvalois/scraping/assets/32735527/70978658-fb1e-48ef-bc42-11469812fef1)
