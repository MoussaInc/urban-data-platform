# 🌍 Urban Data Platform - OSM Analytics

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
* **Python** orchestration / scripts

---

## 📂 Structure du projet

```
dbt/
├── models/
│   ├── staging/
│   │   └── stg_osm_features.sql
│   ├── marts/
│   │   ├── building.sql
│   │   ├── amenities.sql
│   │   └── roads.sql
```

---

## 📊 Modèles principaux

### Staging

* `stg_osm_features` : nettoyage et transformation des données OSM

### Marts

* `building` : bâtiments extraits
* `amenities` : services (écoles, hôpitaux, etc.)
* `roads` : réseau routier

---

## 📈 Cas d’usage

* Analyse urbaine
* Cartographie des infrastructures
* Études de densité (bâtiments, routes, services)

---

## 📌 Améliorations futures

* Ajout de KPI (densité urbaine, accessibilité)
* Dashboard (Looker Studio / Streamlit)
* Orchestration (Kestra / Airflow)

---

## 👤 Auteur

Moussa MBALLO
Ingénieur Génie Civil & Data Engineer
