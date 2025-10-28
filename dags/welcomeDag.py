from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.decorators import dag
from datetime import timedelta

default_args = {
    'owner': 'marcus',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def Hello(name: str):
    print(f"Hello {name}")

@dag(dag_id="test_dag", default_args=default_args, catchup=False, tags=['test_dag'])
def welcome_dag():

    start = BashOperator(
        task_id='start_time', 
        bash_command='date > /opt/airflow/test.txt'
    )
    greet = PythonOperator(
        task_id='greet_task',
        python_callable=Hello,
        op_args=['Airflow User'],
    )

    end = BashOperator(
        task_id='bash_task',
        bash_command='echo "This is a bash task!"',
    )

    start >> greet >> end

welcome_dag()