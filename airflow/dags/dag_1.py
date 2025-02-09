"""
Test dddd
"""

from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import (
    PythonOperator,
    PythonVirtualenvOperator,
    ExternalPythonOperator,
)
from tasks import task_1
from airflow.decorators import task


def callable_virtualenv():
    print("123")


@task.virtualenv(
    task_id="virtualenv_python_2",
    requirements="requirements.txt",
    system_site_packages=False,
)
def callable_virtualenv_2():
    import sys

    sys.path.insert(0, "/opt/airflow/dags")

    from tasks.proj.src.main import func_1

    func_1()


def callable_external_python():
    import polars as pl

    df = pl.DataFrame({"a": [1, 2]})
    print(df)


with DAG(
    "dag_1",
    description="A simple example DAG",
    schedule=timedelta(minutes=30),
    start_date=datetime(year=2025, month=2, day=9),
    tags=["dag_1"],
    doc_md=__doc__,
    catchup=True,
    template_searchpath=["/opt/airflow/dags/tasks/proj"],
) as dag:
    start = EmptyOperator(task_id="start")
    hello = BashOperator(
        task_id="hello",
        bash_command="pwd",
    )
    task_1 = PythonOperator(
        task_id="task_1",
        python_callable=task_1.func_1,
        # op_kwargs: Optional[Dict] = None,
        # op_args: Optional[List] = None,
        # templates_dict: Optional[Dict] = None
        # templates_exts: Optional[List] = None
    )
    virtualenv_task = PythonVirtualenvOperator(
        task_id="virtualenv_python",
        python_callable=callable_virtualenv,
        # requirements=["polars==1.22.0"],
        requirements="requirements.txt",
        system_site_packages=False,
    )
    virtualenv_task_2 = callable_virtualenv_2()
    external_python_task = ExternalPythonOperator(
        task_id="external_python",
        python_callable=callable_external_python,
        python=os.fspath("/opt/airflow/dags/tasks/proj/.venv/Scripts/activate"),
    )
    end = EmptyOperator(task_id="end")

(start >> virtualenv_task >> virtualenv_task_2 >> end)
