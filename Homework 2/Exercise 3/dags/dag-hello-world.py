from airflow import DAG
from datetime import datetime, timedelta 
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task 

default_args = {
    'owner':'chowsonice',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def hello_world():
    print(f"hello world")

with DAG(
    dag_id='python_operator_exercise_v6',
    description='Exercise for dags with python operator',
    default_args=default_args,
    start_date=datetime(2024,5,27,11),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id="task1",
        python_callable=hello_world
    )
    task1