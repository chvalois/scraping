from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from functions.scraping_superimmo import daily_scraping
from functions.inject_to_postgres import add_scraped_data_to_postgresDB
from datetime import datetime, timedelta

my_dag = DAG(
    dag_id='daily_scraping_42',
    description='scraps ads daily on Superimmo website',
    tags=['scraping', 'superimmo'],
    #schedule_interval='0 0-23/4 * * *',
    schedule_interval='0 4 * * *',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1),
    }
)


today = datetime.now().strftime("%Y-%m-%d")
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

task_1 = PythonOperator(
    task_id='daily_scraping_42',
    python_callable=daily_scraping,
    op_kwargs= {
        'dept': 42,
        'region_dept': 'aquitaine/landes',
        'start_date': yesterday,
        'nb_pages': "max"
    },
    dag=my_dag
)

task_2 = PythonOperator(
    task_id='inject_in_postgres',
    python_callable=add_scraped_data_to_postgresDB,
    op_kwargs= {
        'dept': 42,
        'date': yesterday
    },
    dag=my_dag
)

task_3 = BashOperator(
    task_id='run_dbt',
    bash_command='cd /opt/airflow/scraping_dbt && dbt run --profiles-dir /opt/airflow/dbt_profiles',
)

task_1 >> task_2 >> task_3
