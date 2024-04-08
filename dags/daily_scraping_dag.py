from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from functions.scraping_superimmo import daily_scraping
from functions.inject_to_postgres import add_scraped_data_to_postgresDB
from datetime import datetime

my_dag = DAG(
    dag_id='daily_scraping',
    description='scraps ads daily on Superimmo website',
    tags=['scraping', 'superimmo'],
    schedule_interval=None,
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(1),
    }
)


#today = datetime.now().strftime("%Y-%m-%d")
today = "2024-04-06"

task_1 = PythonOperator(
    task_id='daily_scraping_creuse_bis',
    python_callable=daily_scraping,
    op_kwargs= {
        'region_dept': 'limousin/creuse',
        'start_date': today
    },
    dag=my_dag
)


task_2 = PythonOperator(
    task_id='daily_scraping_regiondept_haute-corse',
    python_callable=daily_scraping,
    op_kwargs= {
        'region_dept': 'corse/haute-corse',
        'start_date': today
    },
    dag=my_dag
)

task_3 = PythonOperator(
    task_id='inject_in_postgres',
    python_callable=add_scraped_data_to_postgresDB,
    op_kwargs= {
        'date': today
    },
    dag=my_dag
)

[task_1, task_2] >> task_3