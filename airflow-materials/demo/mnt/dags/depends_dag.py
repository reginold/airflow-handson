from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from pipeline.process import second_task, third_task

default_args = {
    "start_date": datetime(2021, 8, 29),
    "owner": "RDL",
    "email": "owner@test.com",
}


with DAG(
    dag_id="depends_task", schedule_interval="0 0 * * *", default_args=default_args
) as dag:

    # Task 1
    bash_task_1 = BashOperator(task_id="bash_task_1", bash_command="echo 'first task'")

    # Task 2
    python_task_2 = PythonOperator(task_id="python_task_2", python_callable=second_task)

    # Task 3
    python_task_3 = PythonOperator(task_id="python_task_3", python_callable=third_task)

    bash_task_1 >> python_task_2 >> python_task_3
