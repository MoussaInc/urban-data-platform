# dag/urban_dag

from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

# Chemin DBT dans le conteneur Airflow
DBT_PATH = "/opt/airflow/dbt"

default_args = {
    "owner": "mballo",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
}

with DAG(
    dag_id="urban_data_platform_dag",
    default_args=default_args,
    description="Orchestration DBT Urban Data Platform",
    schedule="@daily",
    start_date=datetime(2026, 4, 6),
    catchup=False,
    tags=["dbt", "urban", "osm"],
) as dag:

    # 🔹 Staging
    stg_osm_features = BashOperator(
        task_id="stg_osm_features",
        bash_command=f"cd {DBT_PATH} && dbt run -m stg_osm_features",
    )

    # 🔹 Marts
    building = BashOperator(
        task_id="building",
        bash_command=f"cd {DBT_PATH} && dbt run -m building",
    )

    amenities = BashOperator(
        task_id="amenities",
        bash_command=f"cd {DBT_PATH} && dbt run -m amenities",
    )

    roads = BashOperator(
        task_id="roads",
        bash_command=f"cd {DBT_PATH} && dbt run -m roads",
    )

    # 🔹 Aggregations
    building_by_cities = BashOperator(
        task_id="building_by_cities",
        bash_command=f"cd {DBT_PATH} && dbt run -m building_by_cities",
    )

    amenities_by_city = BashOperator(
        task_id="amenities_by_city",
        bash_command=f"cd {DBT_PATH} && dbt run -m amenities_by_city",
    )

    urban_density_score = BashOperator(
        task_id="urban_density_score",
        bash_command=f"cd {DBT_PATH} && dbt run -m urban_density_score",
    )

    # 🔹 Tests (très important en prod)
    dbt_tests = BashOperator(
        task_id="dbt_tests",
        bash_command=f"cd {DBT_PATH} && dbt test",
    )

    # 🔗 Dépendances
    stg_osm_features >> [building, amenities, roads]

    building >> building_by_cities >> urban_density_score
    amenities >> amenities_by_city >> urban_density_score
    roads >> urban_density_score

    # Tests en fin de pipeline
    urban_density_score >> dbt_tests