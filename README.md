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

- **BigQuery** → Data Warehouse  
- **DBT (Data Build Tool)** → Transformation & modélisation  
- **Airflow** → Orchestration (en cours)  
- **Python** → Scripts & intégration  
- **Streamlit** → Dashboard interactif

---

## Modèles principaux

### Staging
- `stg_osm_features` : nettoyage des données OSM et transformation des tags

### Marts
- `buildings` : données sur les bâtiments  
- `roads` : réseau routier  
- `amenities` : services urbains  
- `urban_density_score` : score d’urbanisation  

---

## KPI & Analyses

- **Buildings by City** → densité urbaine  
- **Amenities by City** → accessibilité aux services  
- **Urban Density Score** → niveau d’urbanisation global  

---

## Cas d’usage

- Identifier les zones urbaines denses  
- Analyser la répartition des services  
- Étudier la corrélation entre infrastructures et urbanisation  

---

## Exécution

### DBT
```bash
dbt run
dbt test
```

### Dashboard
```bash
streamlit run dashboard/app.py
```

### Docker
```bash
docker compose up -d
```

---

## Auteur

**Moussa MBALLO**
Ingénieur Génie Civil & Data Engineer
