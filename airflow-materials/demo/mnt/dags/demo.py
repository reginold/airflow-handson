from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.http.sensors.http import HttpSensor

default_args = {
    "start_date": datetime(2021, 8, 29),
    "owner": "RDL",
    "email": "owner@test.com"
    # "depends_on_past": False,
    # "email": ["airflow@airflow.com"],
    # "email_on_failure": False,
    # "email_on_retry": False,
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

with DAG(dag_id="demo", schedule_interval="@daily", default_args=default_args) as dag:

    # Task 1: check the API available or not
    # reference site:https://airflow.apache.org/docs/apache-airflow-providers-http/stable/operators.html
    is_demo_api_available = HttpSensor(
        task_id="is_demo_api_available",
        method="GET",
        http_conn_id="demo_api",
        endpoint="marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b",
        response_check=lambda response: "rates" in response.text,
        # Time in seconds that the job should wait in between each tries
        poke_interval=5,
        timeout=200,
    )
    # Task 2: 
    bash_task_2 = BashOperator(
        task_id="bash_task_2",
        bash_command='echo "Hello, World!"',
    )

    is_demo_api_available >> bash_task_2
