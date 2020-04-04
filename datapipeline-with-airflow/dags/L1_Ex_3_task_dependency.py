import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def hello_world():
    '''
    Desc : This function prints a string
    '''
    logging.info("Hello World")


def addition():
    '''
    Desc : This function provides result of addition of 2 with 2
    '''
    logging.info(f"2 + 2 = {2+2}")


def subtraction():
    '''
    Desc : This function provides result of subtraction of 2 from 6
    '''
    logging.info(f"6 -2 = {6-2}")


def division():
    '''
    Desc : This function provides result of divison of 10 from 2
    '''
    logging.info(f"10 / 2 = {int(10/2)}")


dag = DAG(
    "lesson1.exercise3",
    schedule_interval='@hourly',
    start_date=datetime.datetime.now() - datetime.timedelta(days=1))

hello_world_task = PythonOperator(
    task_id="hello_world_task",
    python_callable=hello_world,
    dag=dag)


addition_task = PythonOperator(
    task_id="addition_task",
    python_callable=addition,
    dag=dag)

subtraction_task = PythonOperator(
    task_id="subtraction_task",
    python_callable=subtraction,
    dag=dag)

division_task = PythonOperator(
    task_id="division_task",
    python_callable=division,
    dag=dag)

#
# TODO: Configure the task dependencies such that the graph looks like the following:
#
#                    ->  addition_task
#                   /                 \
#   hello_world_task                   -> division_task
#                   \                 /
#                    ->subtraction_task

hello_world_task >> addition_task
hello_world_task >> subtraction_task
addition_task >> division_task
subtraction_task >> division_task