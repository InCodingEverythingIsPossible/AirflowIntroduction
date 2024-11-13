from airflow import DAG

# Operator always connect with hook
# Hook connect to the service and make operation from operator
# You can also call hook directly, and you have more functionality
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

import json
from pandas import json_normalize
from datetime import datetime


def process_user(ti):
    user = ti.xcom_pull(task_ids='extract_user')
    user = user['results'][0]

    processed_user = json_normalize({
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
    })
    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)


def store_user():
    hook = PostgresHook(postgres_conn_id='postgres')

    hook.copy_expert(
        sql="COPY users FROM stdin WITH DELIMITER as ','",
        filename='/tmp/processed_user.csv'
    )


# dag_id -> must be unique across all dags
# start_date -> start date of when dag will start running
# schedule_interval -> occurrence of running dag
#           https://airflow.apache.org/docs/apache-airflow/1.10.10/scheduler.html#dag-runs
# catchup -> will launch outstanding executions that have not performed from start_date to now
with DAG(
        dag_id='user_processing',
        start_date=datetime(2022, 1, 1),
        schedule_interval='@daily',
        catchup=False
) as dag:
    # task_id -> unique task_id across all tasks inside same dag
    # postgres_conn_id -> connection id to connect with postgres database
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS users(
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )

    extract_user = SimpleHttpOperator(
        task_id='extract_user',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    process_user = PythonOperator(
        task_id='process_user',
        python_callable=process_user
    )

    store_user = PythonOperator(
        task_id='store_user',
        python_callable=store_user
    )

    # Make dependencies of tasks

    create_table >> is_api_available >> extract_user >> process_user >> store_user


