import os
from airflow.models import DagBag

dags_folder = os.path.join(os.path.dirname(__file__), "../dags")

def validate_dags():
    dag_bag = DagBag(dag_folder=dags_folder)
    if dag_bag.import_errors:
        print("dag can't load:")
        for dag_id, error in dag_bag.import_errors.items():
            print(f"{dag_id}: {error}")
        exit(1)
    else:
        print("all dags loaded successfully")

if __name__ == "__main__":
    validate_dags()