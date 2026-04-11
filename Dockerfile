FROM apache/airflow:2.7.2

USER root
RUN apt-get update && apt-get install -y git && apt-get clean

USER airflow
RUN pip install --no-cache-dir dbt-bigquery==1.7.0
