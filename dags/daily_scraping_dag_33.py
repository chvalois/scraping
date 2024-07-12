from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from functions.scraping_superimmo import daily_scraping
from functions.inject_to_postgres import add_scraped_data_to_postgresDB
from datetime import datetime, timedelta

dept = 33
region_dept = 'aquitaine/gironde'

my_dag = DAG(
    dag_id=f'daily_scraping_{dept}',
    description='scraps ads daily on Superimmo website',
    tags=['scraping', 'superimmo'],
    schedule_interval='10 2 * * *',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(1),
    }
)

today = datetime.now().strftime("%Y-%m-%d")
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

task_1 = PythonOperator(
    task_id=f'daily_scraping_{dept}',
    python_callable=daily_scraping,
    retries=2,
    retry_delay=timedelta (seconds=30),
    op_kwargs= {
        'dept': dept,
        'region_dept': region_dept,
        'start_date': yesterday,
        'nb_pages': "max"
    },
    dag=my_dag
)

task_2 = PythonOperator(
    task_id=f'inject_in_postgres_{dept}',
    python_callable=add_scraped_data_to_postgresDB,
    op_kwargs= {
        'dept': dept,
        'date': yesterday
    },
    dag=my_dag
)

task_3 = BashOperator(
    task_id='run_dbt',
    retries=2,
    retry_delay=timedelta (seconds=30),
    bash_command='cd /opt/airflow/scraping_dbt && dbt run --profiles-dir /opt/airflow/dbt_profiles',
)

task_1 >> task_2 >> task_3
