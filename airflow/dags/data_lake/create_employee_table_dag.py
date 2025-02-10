# """
# Create Eemployee Table DAG
# """
from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {"start_date": datetime.now()}


@dag(
    "create_employee_table_dag",
    description="Create Employee Table DAG",
    schedule=timedelta(minutes=1000),
    default_args=default_args,
    template_searchpath=["/opt/airflow/dags/data_lake/create_employee_table"],
    catchup=False,
)
def taskflow():
    @task(task_id="start")
    def start() -> None:
        return None

    @task.virtualenv(
        task_id="python",
        requirements="requirements.txt",
        system_site_packages=False,
    )
    def python(func) -> None:
        import sys

        sys.path.insert(0, "/opt/airflow/dags/data_lake/create_employee_table/src")

        from main import main

        main()
        return None

    @task(task_id="end")
    def end(func) -> None:
        return None

    end(python(start()))


taskflow()
