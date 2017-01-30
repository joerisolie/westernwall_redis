from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(minutes=1),
    'email': ['joerisolie@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def conditionally_trigger(context, dag_run_obj):
    return dag_run_obj

dag = DAG(dag_id='wrapperJSO', default_args=default_args, schedule_interval=timedelta(minutes=1))

trigger = TriggerDagRunOperator(task_id='dag1', trigger_dag_id='tutorialJSO3',python_callable=conditionally_trigger,dag=dag)
