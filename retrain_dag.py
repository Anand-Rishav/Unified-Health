from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG('retrain_if_drift', start_date=datetime(2025,7,19),
         schedule_interval='@daily', catchup=False) as dag:
    drift   = BashOperator(task_id='detect_drift', bash_command='python check_drift.py')
    retrain = BashOperator(task_id='retrain',     bash_command='python retrain.py',
                           trigger_rule='one_failed')
    drift >> retrain
