# Urban Data Platform — OSM Analytics

> Pipeline ELT de bout en bout sur des données OpenStreetMap : ingestion, transformation dbt, orchestration Airflow, visualisation Streamlit — le tout déployé sur Google Cloud.

[![CI](https://github.com/MoussaInc/urban-data-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/MoussaInc/urban-data-platform/actions/workflows/ci.yml)
![dbt](https://img.shields.io/badge/dbt-1.7-orange)
![BigQuery](https://img.shields.io/badge/BigQuery-GCP-blue)
![Airflow](https://img.shields.io/badge/Airflow-2.7-red)
![Python](https://img.shields.io/badge/Python-3.12-green)

---

## Aperçu

Ce projet analyse la densité urbaine de villes du monde entier à partir des données publiques OpenStreetMap. Il produit un score d'urbanisation par ville en croisant trois dimensions : bâtiments, équipements (amenities) et réseau routier.

```
OpenStreetMap (BigQuery public dataset)
        │
        ▼
  stg_osm_features        ← nettoyage & typage
        │
   ┌────┴────┐
   ▼         ▼         ▼
building  amenities  roads  ← modèles intermédiaires
   │         │         │
   ▼         ▼         │
building_  amenities_  │
by_cities  by_city     │
   │         │         │
   └────┬────┘─────────┘
        ▼
 urban_density_score        ← mart final
        │
        ▼
  Dashboard Streamlit
```

---

## Stack technique

| Couche | Outil | Rôle |
|---|---|---|
| Data Warehouse | BigQuery (GCP) | Stockage & requêtage |
| Transformation | dbt 1.7 | Modélisation ELT, tests, documentation |
| Orchestration | Apache Airflow 2.7 | Scheduling du pipeline |
| Containerisation | Docker Compose | Environnement reproductible |
| Visualisation | Streamlit + Plotly | Dashboard interactif |
| CI/CD | GitHub Actions | Tests automatisés à chaque push |
| Package manager | uv | Gestion des dépendances Python |

---

## Structure du projet

```
urban-data-platform/
├── dag/
│   ├── urban_dag.py          # DAG Airflow — orchestration du pipeline
│   └── test_urban_dag.py     # Tests unitaires du DAG (pytest)
├── dbt/
│   ├── models/
│   │   ├── staging/          # stg_osm_features
│   │   ├── core/             # building, amenities, roads
│   │   └── marts/            # building_by_cities, amenities_by_city,
│   │                         # urban_density_score
│   └── tests/                # Tests singuliers SQL
├── dashboard/
│   ├── app.py                # Point d'entrée Streamlit
│   ├── style.css             # Styles CSS
│   └── utils/
│       ├── data.py           # Chargement BigQuery & filtres
│       ├── charts.py         # Graphiques Plotly
│       └── components.py     # Composants UI réutilisables
├── Dockerfile                # Image Airflow + dbt-bigquery
├── docker-compose.yml        # Stack complète
└── pyproject.toml            # Dépendances & config pytest
```

---

## Modèles dbt

### Staging
`stg_osm_features` — nettoyage des données brutes OSM : typage des colonnes, extraction des tags JSON, filtrage des géométries invalides.

### Core
- `building` — bâtiments par ville avec surface et type
- `amenities` — équipements urbains (écoles, hôpitaux, commerces...)
- `roads` — réseau routier par ville

### Marts
- `building_by_cities` — agrégation du nombre de bâtiments par ville
- `amenities_by_city` — agrégation des équipements par ville
- `urban_density_score` — score composite normalisé croisant les trois dimensions

### Tests dbt
Chaque modèle est couvert par des tests `not_null`, `unique`, `accepted_values` et des tests singuliers SQL pour la cohérence métier (géométries valides, surfaces positives, coordonnées dans les plages attendues).

---

## DAG Airflow

Le pipeline est orchestré par un DAG quotidien avec gestion des dépendances parallèles :

```
stg_osm_features
      │
 ┌────┼────┐
 ▼    ▼    ▼
 bld  ami  roads
 │    │      │
 ▼    ▼      │
bld_ ami_    │
by_  by_     │
city city    │
 │    │      │
 └────┴──────┘
        ▼
urban_density_score
        ▼
    dbt test
```

---

## Lancer le projet

### Prérequis
- Docker & Docker Compose
- Compte GCP avec BigQuery activé
- Credentials GCP (`application_default_credentials.json`)

### Démarrage

```bash
# 1. Cloner le repo
git clone https://github.com/MoussaInc/urban-data-platform.git
cd urban-data-platform

# 2. Initialiser Airflow
docker compose up airflow-init

# 3. Lancer la stack complète
docker compose up -d

# 4. Accéder aux interfaces
# Airflow   → http://localhost:8080  (admin / admin)
# Streamlit → http://localhost:8501
```

### Tests

```bash
# Tests unitaires du DAG
pytest dag/ -v

# Tests dbt
cd dbt/
dbt test
```

---

## CI/CD

Chaque push sur `main` ou `develop` déclenche automatiquement :

1. **Tests DAG** — validation de la structure et des dépendances du DAG Airflow
2. **Tests dbt** — compilation, run staging, tests sur BigQuery

---

## Dashboard

Le dashboard Streamlit visualise les résultats du pipeline :

- KPIs globaux (nombre de villes, score moyen, totaux)
- Classement des villes par score de densité urbaine
- Radar de composition (bâtiments / équipements / routes)
- Corrélation bâtiments vs équipements
- Filtres par pays et top N dynamique

---

## Auteur

**Moussa MBALLO** — Ingénieur Génie Civil & Data Engineer

[![GitHub](https://img.shields.io/badge/GitHub-MoussaInc-181717?logo=github)](https://github.com/MoussaInc/urban-data-platform)