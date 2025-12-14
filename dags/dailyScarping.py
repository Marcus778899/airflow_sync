from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
import pendulum
from datetime import timedelta
import json

TARGET_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
CONN_ID = "spring_boot_api"
TZ = pendulum.timezone("UTC")

default_args = {
    'owner': 'marcus',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,             
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='binance_kline_sync_v1',
    default_args=default_args,
    description='Sync historical and daily kline data from Binance',
    schedule='@daily',
    start_date=pendulum.datetime(2020, 1, 1, tz=TZ),
    catchup=True,                   
    max_active_runs=1,               
    tags=['binance', 'core', 'kline'],
) as dag:
    for symbol in TARGET_SYMBOLS:
        payload = {
            "symbol": symbol,
            "interval": "1m",
            "startTime": "{{ data_interval_start.isoformat() }}",
            "endTime": "{{ data_interval_end.isoformat() }}"
        }

        HttpOperator(
            task_id=f'sync_{symbol.lower()}',
            http_conn_id=CONN_ID,
            endpoint='/api/v1/batch/klines',
            method='POST',
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            response_check=lambda response: response.status_code == 202,
            log_response=True
        )