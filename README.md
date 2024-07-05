# Generate a database of real estate ads

This project enables to generate a whole automatically updated real estate ads database.
The final goal is to be able to analyze the evolution of the real estate market using Metabase.

Here is how it works: 
![image](https://github.com/chvalois/scraping/assets/32735527/228926fe-5e4e-4312-bf71-7ed08e508f66)


## Where do I start?

### 1. Initiate Airflow and Postgres services through Docker-Compose

```
docker-compose up -d
```

### 2. Connect to the database "scraping_db" and create the table "ads"

```
docker container exec -it airflow_scheduler psql -h postgres-db -U chvalois -d scraping_db -f files/project_init_sql.pgsql

```

### 3. Initiate dbt

```
docker container exec -it airflow_scheduler bash
cd scraping_dbt
dbt init --profiles-dir /opt/airflow/dbt_profiles
dbt seed --profiles-dir /opt/airflow/dbt_profiles
dbt run --profiles-dir /opt/airflow/dbt_profiles
psql -h postgres-db -U chvalois -d scraping_db -c "ALTER TABLE src_ads_cleaned REPLICA IDENTITY FULL;"
```

### 4. Access tools

```
# Airflow
localhost:8080

# Grafana 
localhost:3001

# Metabase
localhost:3002

# pgAdmin
localhost:5050
```


## Data Flow

### 1. Airflow will scrap a website containing ads everyday at 4AM UTC and then inject data in a PostgresDB
 
### 2. dbt transforms data inside PostgresDB
![2024 04 09 - 6942 - 1615x372](https://github.com/chvalois/scraping/assets/32735527/70978658-fb1e-48ef-bc42-11469812fef1)

### 3. Data can be queried in Metabase

