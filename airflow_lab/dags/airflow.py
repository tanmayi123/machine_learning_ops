# Import necessary libraries and modules
from airflow import DAG
# from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
from airflow.utils.email import send_email # type: ignore
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow, generate_dashboard
import os
# NOTE:
# In Airflow 3.x, enabling XCom pickling should be done via environment variable:
# export AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
# The old airflow.configuration API is deprecated.

def notify_success(context):
    dag_id = context['dag'].dag_id
    run_id = context['run_id']
    send_email(
        to=os.environ.get('ALERT_EMAIL'),
        subject=f' DAG Success: {dag_id}',
        html_content=f"""
        <h3>DAG completed successfully!</h3>
        <b>DAG:</b> {dag_id}<br>
        <b>Run ID:</b> {run_id}<br>
        <b>Time:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
        """
    )

def notify_failure(context):
    dag_id = context['dag'].dag_id
    task_id = context['task_instance'].task_id
    run_id = context['run_id']
    send_email(
        to=os.environ.get('ALERT_EMAIL'),
        subject=f' DAG Failed: {dag_id}',
        html_content=f"""
        <h3>DAG task failed!</h3>
        <b>DAG:</b> {dag_id}<br>
        <b>Failed Task:</b> {task_id}<br>
        <b>Run ID:</b> {run_id}<br>
        <b>Time:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
        """
    )

# Define default arguments for your DAG
default_args = {
    'owner': 'Tanmayi',
    'start_date': datetime(2026, 1, 15),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': notify_failure,
  # Delay before retries
}

# Create a DAG instance named 'Airflow_Lab1' with the defined default arguments
with DAG(
    'Airflow_Lab1',
    default_args=default_args,
    description='Dag example for Lab 1 of Airflow series',
    catchup=False,
    on_success_callback=notify_success,
) as dag:
    # Task to load data, calls the 'load_data' Python function
    load_data_task = PythonOperator(
        task_id='load_data_task',
        python_callable=load_data,
    )

    # Task to perform data preprocessing, depends on 'load_data_task'
    data_preprocessing_task = PythonOperator(
        task_id='data_preprocessing_task',
        python_callable=data_preprocessing,
        op_args=[load_data_task.output],
    )

    # Task to build and save a model, depends on 'data_preprocessing_task'
    build_save_model_task = PythonOperator(
        task_id='build_save_model_task',
        python_callable=build_save_model,
        op_args=[data_preprocessing_task.output, "model.sav"],
    )

    # Task to load a model using the 'load_model_elbow' function, depends on 'build_save_model_task'
    load_model_task = PythonOperator(
        task_id='load_model_task',
        python_callable=load_model_elbow,
        op_args=["model.sav", build_save_model_task.output],
    )

    # Set task dependencies
    # Task to generate HTML dashboard
    generate_dashboard_task = PythonOperator(
        task_id='generate_dashboard_task',
        python_callable=generate_dashboard,
        op_args=[
            data_preprocessing_task.output,
            build_save_model_task.output,
            load_model_task.output,
        ],
    )

    # Set task dependencies
    load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task >> generate_dashboard_task

# If this script is run directly, allow command-line interaction with the DAG
if __name__ == "__main__":
    dag.test()

