from airflow import DAG
from airflow.operators.bash_operator import BashOperator
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

dag = DAG('tutorialJSO3', default_args=default_args, schedule_interval=None)

t1 = BashOperator(
    task_id = 'print_date',
    bash_command = 'date',
    dag = dag
)

t2 = BashOperator(
    task_id = 'sleep',
    bash_command = 'sleep 5',
    retries = 3,
    dag = dag
)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in JSO'},
    dag = dag
)

t2.set_upstream(t1)
t3.set_upstream(t1)