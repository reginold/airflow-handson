# from datetime import datetime

# # import boto3
# from airflow import DAG
# from airflow.operators.python import PythonOperator

# ACCESS_KEY = "AKIA5LZQ2CELLJW7FK3Q"
# SECRET_KEY = "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"
# REGION_NAME = "ap-northeast-1"


# def upload_file():
#     """push the file to s3"""
#     client = boto3.client(
#         "s3",
#         aws_access_key=ACCESS_KEY,
#         aws_secret_access_key=SECRET_KEY,
#         region_name=REGION_NAME,
#     )

#     with open("/usr/local/airflow/dags/test.csv", "rb") as f:
#         client.upload_fileobj(f, "lu-airflow", "test.csv")

#     print("Upload Completed")
#     print("........")


# default_args = {
#     "start_date": datetime(2021, 9, 29),
#     "owner": "RDL",
#     "email": "owner@test.com",
# }


# with DAG(
#     dag_id="upload_s3", schedule_interval="0 0 * * *", default_args=default_args
# ) as dag:

#     # Task 1
#     bash_task_1 = PythonOperator(
#         task_id="bash_task_1",
#         python_callable=upload_file,
#     )
