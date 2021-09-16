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
    down_dataset = BashOperator(
        task_id="down_dataset",
        bash_command="python ~/dags/pipeline/download_data_airflow.py",
    )

    # Task 2
    make_dataset = BashOperator(
        task_id="make_dataset",
        bash_command="python ~/dags/pipeline/make_dataset_airflow.py",
    )

    # Task 3
    clean_dataset = BashOperator(
        task_id="clean_dataset",
        bash_command="python ~/dags/pipeline/clean_data_airflow.py",
    )

    down_dataset >> make_dataset >> clean_dataset
