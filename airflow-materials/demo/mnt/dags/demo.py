import csv
import json
from datetime import datetime

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor

default_args = {
    "start_date": datetime(2021, 9, 14),
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


def download_rates():
    BASE_URL = "https://gist.githubusercontent.com/marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b/raw/"
    ENDPOINTS = {
        "USD": "api_forex_exchange_usd.json",
        "EUR": "api_forex_exchange_eur.json",
    }
    with open("/usr/local/airflow/dags/files/jobCode_ref.csv") as jobCode_ref:
        reader = csv.DictReader(jobCode_ref, delimiter=";")
        for idx, row in enumerate(reader):
            base = row["base"]
            with_pairs = row["with_pairs"].split(" ")
            indata = requests.get(f"{BASE_URL}{ENDPOINTS[base]}").json()
            outdata = {"base": base, "rates": {}, "last_update": indata["date"]}
            for pair in with_pairs:
                outdata["rates"][pair] = indata["rates"][pair]
            with open("/usr/local/airflow/dags/files/rates.json", "a") as outfile:
                json.dump(outdata, outfile)
                outfile.write("\n")


with DAG(dag_id="demo", schedule_interval="@daily", default_args=default_args) as dag:

    # Task 1: check the API is available or not
    # reference site:https://airflow.apache.org/docs/apache-airflow-providers-http/stable/operators.html
    is_demo_api_available = HttpSensor(
        task_id="is_demo_api_available",
        method="GET",
        http_conn_id="demo_api",
        endpoint="marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b",
        response_check=lambda response: "rates" in response.text,
        # Time in seconds that the job should wait in between each tries
        poke_interval=5,
        timeout=20,
    )
    # Task 2: check the FILE is avaliable or not
    is_jobCode_ref_file_available = FileSensor(
        task_id="is_jobCode_ref_file_available",
        fs_conn_id="jobCode_ref_path",
        filepath="jobCode_ref.csv",
        poke_interval=5,
        timeout=20,
    )

    downloading_rates = PythonOperator(
        task_id="downloading_rates", python_callable=download_rates
    )

    is_demo_api_available >> is_jobCode_ref_file_available >> downloading_rates
