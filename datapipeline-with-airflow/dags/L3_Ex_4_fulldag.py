import datetime

from airflow import DAG

from airflow.operators import (
    FactsCalculatorOperator,
    HasRowsOperator,
    S3ToRedshiftOperator
)

#
# TODO: Create a DAG which performs the following functions:
#
#       1. Loads Trip data from S3 to RedShift
#       2. Performs a data quality check on the Trips table in RedShift
#       3. Uses the FactsCalculatorOperator to create a Facts table in Redshift

dag = DAG("lesson3.exercise4", start_date=datetime.datetime.utcnow())


#Load trips data from S3 to RedShift. Use the s3_key
#       "data-pipelines/divvy/unpartitioned/divvy_trips_2018.csv"
#       and the s3_bucket "udacity-dend"

copy_trips_task = S3ToRedshiftOperator(
    task_id="load_trips_from_s3_to_redshift",
    dag=dag,
    table="trips",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="data-pipelines/divvy/unpartitioned/divvy_trips_2018.csv"
)

#Perform a data quality check on the Trips table

check_trips = HasRowsOperator(
    task_id="trips_has_rows",
    dag=dag,
    redshift_conn_id="redshift",
    table="trips",
    provide_context=True
)

#Use the FactsCalculatorOperator to create a Facts table in RedShift. The #fact column should be `tripduration` and the groupby_column should be #`bikeid`

calculate_facts = FactsCalculatorOperator(
    task_id="calculate_facts",
    dag=dag,
    postgres_conn_id="redshift",
    origin_table="trips",
    destination_table="trips_facts",
    fact_column="tripduration",
    groupbycolumn="bikeid"
)

#Define task ordering for the DAG tasks you defined
copy_trips_task >> check_trips
check_trips >> calculate_facts
