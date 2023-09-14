from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

import os
import sys
home = os.environ['FORECAST_PROJECT_HOME']
sys.path.append(home)
from config import owner
from src.fetch.fetch_weather_data import fetch_data
from src.ingest.data_from_csv_to_sql import ingest_data

default_args = {
    'owner': owner,
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
    'start_date' : datetime(2023,8,8),
    'schedule':timedelta(minutes=1), # run daily 
    'catchup':False
}
dag = DAG('weather_data_dag', default_args=default_args)

fetch=PythonOperator(task_id='fetch_weather_data',
                            python_callable= fetch_data,
                            dag=dag)

ingest=PythonOperator(task_id='ingest_weather_data',
                            python_callable=ingest_data,
                            dag=dag)

transform = BashOperator(task_id='transform_weather_data',
                        bash_command='dbt run',
                        dag=dag)
    
fetch >> ingest >> transform