from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "start_date": datetime(2021, 9, 15),
    "owner": "RDL",
    "email": "owner@test.com",
}


with DAG(
    dag_id="depends_task", schedule_interval="0 0 * * *", default_args=default_args
) as dag:

    # Task 1
    bash_task_1 = BashOperator(
        task_id="bash_task_1",
        bash_command="python ~/dags/pipeline/download_data_airflow.py",
    )
    # Task 2
    # bash_task_2 = BashOperator(
    #     task_id="bash_task_2",
    #     bash_command="python ~/dags/pipeline/make_dataset_airflow.py",
    # )

    # bash_task_1 >> bash_task_2
