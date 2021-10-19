from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "start_date": datetime(2021, 10, 18),
    "owner": "RDL",
    "email": "owner@test.com",
}


with DAG(
    dag_id="depends_task", schedule_interval="0 0 * * *", default_args=default_args
) as dag:

    # Task 1: Download the data
    download_dataset = BashOperator(
        task_id="download_dataset",
        bash_command="python ~/dags/pipeline/download_data_airflow.py",
    )

    # Task 2: Make the data
    make_dataset = BashOperator(
        task_id="make_dataset",
        bash_command="python ~/dags/pipeline/make_dataset_airflow.py",
    )

    # Task 3: Clean the data
    clean_dataset = BashOperator(
        task_id="clean_dataset",
        bash_command="python ~/dags/pipeline/clean_data_airflow.py",
    )

    # Task 4: Extract feature
    extract_feature = BashOperator(
        task_id="extract_feature",
        bash_command="python ~/dags/pipeline/extract_feature_airflow.py",
    )

    # Task 5: Transform data
    transform_data = BashOperator(
        task_id="transform_data",
        bash_command="python ~/dags/pipeline/transform_data_airflow.py",
    )

    # Task 6: impute_datasets
    impute_datasets = BashOperator(
        task_id="impute_datasets",
        bash_command="python ~/dags/pipeline/impute_data_airflow.py",
    )

    # Task 7: train model
    train_model = BashOperator(
        task_id="train_model",
        bash_command="python ~/dags/pipeline/train_model_airflow.py",
    )

    # Task 8: evaluate model
    evaluate_model = BashOperator(
        task_id="evaluate_model",
        bash_command="python ~/dags/pipeline/evaluate_model_airflow.py",
    )
    download_dataset >> make_dataset >> clean_dataset
    clean_dataset >> extract_feature >> transform_data
    transform_data >> impute_datasets >> train_model >> evaluate_model
