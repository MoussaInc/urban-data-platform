# Urban Data Platform - OSM Analytics

## Description

Ce projet est un pipeline de data engineering basé sur OpenStreetMap (OSM), permettant de transformer des données brutes en tables prêtes pour l’analyse.

L’objectif est de construire une architecture moderne avec DBT et BigQuery pour analyser des données urbaines (bâtiments, routes, services, etc.).

---

## Architecture

Le pipeline suit une logique ELT :

```
Raw Data (BigQuery public dataset)
        ↓
Staging (osm_staging)
        ↓
Marts (osm_marts)
        ↓
Analytics / Dashboard
```

---

## Stack technique

* **BigQuery** → Data warehouse
* **DBT** → Transformation des données
* **SQL** → Modélisation
* **Python** → Scripts / orchestration

---

## Structure du projet

```
.
├── dashboard
│   └── app.py
├── dbt
│   ├── dbt_packages
│   ├── dbt_project.yml
│   ├── logs
│   │   └── dbt.log
│   ├── models
│   │   ├── core
│   │   ├── marts
│   │   │   ├── amenities_by_city.sql
│   │   │   ├── amenities.sql
│   │   │   ├── building_by_cities.sql
│   │   │   ├── building.sql
│   │   │   ├── roads.sql
│   │   │   ├── schema.yml
│   │   │   └── urban_density_score.sql
│   │   └── staging
│   │       └── stg_osm_features.sql
│   ├── target
│   │   ├── ....
│   │   ├── ....
│   └── tests
├── docs
├── logs
│   └── dbt.log
├── orchestration
├── pyproject.toml
├── README.md
├── sql
└── uv.lock
```

---

## Modèles principaux

### Staging

* `stg_osm_features` : nettoyage et transformation des données OSM (flatten des tags)


## KPI & Analyses

* **Buildings by City :** densité de bâtiments
* **Amenities by City :** accessibilité aux services
* **Urban Density Score :** score d’urbanisation basé sur :

  * bâtiments
  * services
  * routes

---

## Insights

* Les grandes villes concentrent-elles la majorité des services (amenities) ?
* Existe-t-il une forte corrélation entre densité de bâtiments et réseau routier ?
* Est-il possible d’identifier les zones urbaines majeures (score d’urbanisation) ?

---

## Exécution

### Lancer les modèles DBT

```
dbt run
```

### Lancer les tests

```
dbt test
```

---

## Améliorations futures

* Orchestration (Kestra / Airflow)

---

## Dashboard (Streamlit)

Lancer le dashboard en local :

```bash
streamlit run dashboard/app.py
```

## Auteur

**Moussa MBALLO**
Ingénieur Génie Civil & Data Engineer
