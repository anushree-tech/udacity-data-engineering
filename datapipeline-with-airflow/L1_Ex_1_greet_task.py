import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def greet():
    '''
    Desc: This function prints a string
    '''
    logging.info('Hello Anushree')


dag = DAG(
        'lesson1.exercise1',
        start_date=datetime.datetime.now())


greet_task = PythonOperator(
    task_id="greet_task",
   python_callable=greet,
    dag= dag
)
