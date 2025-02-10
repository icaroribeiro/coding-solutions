import os

from airflow.models import DagBag

# dags_dirs = ["~/new_dag_bag1", "~/work/new_dag_bag2"]
dags_dirs = ["/opt/airflow/dags/data_lake"]

for dir in dags_dirs:
    dag_bag = DagBag(os.path.expanduser(dir))

    if dag_bag:
        for dag_id, dag in dag_bag.dags.items():
            globals()[dag_id] = dag
