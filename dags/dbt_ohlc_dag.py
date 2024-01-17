"""
The `dbt_ohlc` DAG runs `dbt build` selecting all models tagged with `ohlc` and all of its parents.
The function dbt_task() has `build` as the default argument for `dbt`
and the default graph operator is `+`.
The final command is similar to: `dbt build --select +tag:ohlc`
"""
from airflow import DAG
from kubernetes.client import models as k8s
from stellar_etl_airflow.build_dbt_task import dbt_task
from stellar_etl_airflow.default import get_default_dag_args

dag = DAG(
    "dbt_ohlc",
    default_args=get_default_dag_args(),
    schedule_interval=None,  # don’t schedule since this DAG is externally triggered daily
    user_defined_filters={
        "container_resources": lambda s: k8s.V1ResourceRequirements(requests=s),
    },
    max_active_runs=1,
    catchup=False,
    tags=["dbt"],
)

dbt_ohlc_task = dbt_task(dag, tag="ohlc")