"""
The `enriched_history_operations` DAG runs `dbt build` the `enriched_history_operations` model.
The function dbt_task() has `build` as the default argument for `dbt`
and the default graph operator is `+`.
The final command is similar to: `dbt build --select +enriched_history_operations`
"""
from airflow import DAG
from kubernetes.client import models as k8s
from stellar_etl_airflow.build_dbt_task import dbt_task
from stellar_etl_airflow.default import get_default_dag_args

dag = DAG(
    "enriched_history_operations",
    default_args=get_default_dag_args(),
    schedule_interval=None,  # don’t schedule since this DAG is externally triggered daily
    user_defined_filters={
        "container_resources": lambda s: k8s.V1ResourceRequirements(requests=s),
    },
    max_active_runs=1,
    catchup=False,
    tags=["dbt"],
)

enriched_history_operations_task = dbt_task(
    dag, model_name="enriched_history_operations"
)
