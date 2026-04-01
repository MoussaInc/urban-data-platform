import streamlit as st
from google.cloud import bigquery
import pandas as pd

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="OSM - Urban Data Dashboard",
    layout="wide"
)

st.title("🌍 OSM - Urban Data Dashboard")

# -------------------------------
# CACHE (performance)
# -------------------------------
@st.cache_data
def load_data():
    client = bigquery.Client(project="urban-analytics-osm")

    query_density = """
    SELECT *
    FROM `urban-analytics-osm.osm_marts.urban_density_score`
    """

    query_amenities = """
    SELECT *
    FROM `urban-analytics-osm.osm_marts.amenities_by_city`
    """

    query_buildings = """
    SELECT *
    FROM `urban-analytics-osm.osm_marts.building_by_cities`
    """

    df_density = client.query(query_density).to_dataframe()
    df_amenities = client.query(query_amenities).to_dataframe()
    df_buildings = client.query(query_buildings).to_dataframe()

    return df_density, df_amenities, df_buildings


df_density, df_amenities, df_buildings = load_data()

# -------------------------------
# FILTRES
# -------------------------------
st.sidebar.header("Filtres")

countries = df_density["country"].dropna().unique()
selected_country = st.sidebar.selectbox("Choisir un pays", countries)

df_filtered = df_density[df_density["country"] == selected_country]

# -------------------------------
# KPI
# -------------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Nb villes", len(df_filtered))
col2.metric("Score moyen", round(df_filtered["urban_density_score"].mean(), 2))
col3.metric("Score max", round(df_filtered["urban_density_score"].max(), 2))

# -------------------------------
# TABLE + GRAPH
# -------------------------------
st.subheader(f"🏙️ Villes en {selected_country}")

st.dataframe(df_filtered)

st.bar_chart(
    df_filtered.set_index("city")["urban_density_score"]
)

# -------------------------------
# TOP 10
# -------------------------------
st.subheader("🔝 Top 10 villes")

top10 = df_filtered.sort_values(
    by="urban_density_score", ascending=False
).head(10)

st.dataframe(top10)

st.bar_chart(
    top10.set_index("city")["urban_density_score"]
)

# -------------------------------
# ANALYSE CROISÉE
# -------------------------------
st.subheader("📊 Buildings vs Amenities")

# Merge datasets
df_merge = df_amenities.merge(df_buildings, on="city")

# Optionnel : filtre pays si dispo
if "country" in df_merge.columns:
    df_merge = df_merge[df_merge["country"] == selected_country]

st.scatter_chart(
    df_merge,
    x="num_buildings",
    y="num_amenities"
)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("Projet Data Engineering - OSM Analytics 🚀")