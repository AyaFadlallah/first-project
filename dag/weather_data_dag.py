from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from fetch_weather_data import fetch_data
from data_from_csv_to_sql import ingest_data
from config import owner

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
    
fetch >> ingest