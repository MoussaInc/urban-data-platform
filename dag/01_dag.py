from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

# Paramètres du DAG
default_args = {
    'owner': 'mballo',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'urban_data_platform_dag',
    default_args=default_args,
    description='Orchestration DBT Urban Data Platform',
    schedule_interval='@daily',  # Exécution quotidienne
    start_date=datetime(2026, 4, 6),
    catchup=False,
)

# Étape 1 : Staging
stg_osm_features = BashOperator(
    task_id='dbt_stg_osm_features',
    bash_command='cd /data/projects/data-engineering/urban-data-platform/dbt && dbt run -m stg_osm_features',
    dag=dag,
)

# Étape 2 : Marts
building = BashOperator(
    task_id='dbt_building',
    bash_command='cd /data/projects/data-engineering/urban-data-platform/dbt && dbt run -m building',
    dag=dag,
)

amenities = BashOperator(
    task_id='dbt_amenities',
    bash_command='cd /data/projects/data-engineering/urban-data-platform/dbt && dbt run -m amenities',
    dag=dag,
)

roads = BashOperator(
    task_id='dbt_roads',
    bash_command='cd /data/projects/data-engineering/urban-data-platform/dbt && dbt run -m roads',
    dag=dag,
)

# Étape 3 : KPI et agrégations
building_by_cities = BashOperator(
    task_id='dbt_building_by_cities',
    bash_command='cd /data/projects/data-engineering/urban-data-platform/dbt && dbt run -m building_by_cities',
    dag=dag,
)

amenities_by_city = BashOperator(
    task_id='dbt_amenities_by_city',
    bash_command='cd /data/projects/data-engineering/urban-data-platform/dbt && dbt run -m amenities_by_city',
    dag=dag,
)

urban_density_score = BashOperator(
    task_id='dbt_urban_density_score',
    bash_command='cd /data/projects/data-engineering/urban-data-platform/dbt && dbt run -m urban_density_score',
    dag=dag,
)

# Définition de l’ordre d’exécution
stg_osm_features >> [building, amenities, roads]
building >> building_by_cities >> urban_density_score
amenities >> amenities_by_city
roads >> urban_density_score