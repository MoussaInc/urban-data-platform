import streamlit as st
import pandas as pd
from google.cloud import bigquery

PROJECT = "urban-analytics-osm"

QUERIES = {
    "density": """
        SELECT *
        FROM `urban-analytics-osm.osm_marts.urban_density_score`
        ORDER BY urban_density_score DESC
    """,
    "amenities": """
        SELECT *
        FROM `urban-analytics-osm.osm_marts.amenities_by_city`
        ORDER BY num_amenities DESC
    """,
    "buildings": """
        SELECT *
        FROM `urban-analytics-osm.osm_marts.building_by_cities`
        ORDER BY num_buildings DESC
    """,
}


@st.cache_data(ttl=3600)
def load_all() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    client = bigquery.Client(project=PROJECT)
    df_density   = client.query(QUERIES["density"]).to_dataframe()
    df_amenities = client.query(QUERIES["amenities"]).to_dataframe()
    df_buildings = client.query(QUERIES["buildings"]).to_dataframe()
    return df_density, df_amenities, df_buildings


def filter_by_country(df: pd.DataFrame, country: str) -> pd.DataFrame:
    if country == "Tous" or "country" not in df.columns:
        return df
    return df[df["country"] == country]


def merge_amenities_buildings(
    df_amenities: pd.DataFrame,
    df_buildings: pd.DataFrame,
    country: str,
) -> pd.DataFrame:
    join_cols = ["city", "country"] if "country" in df_amenities.columns else ["city"]
    df = df_amenities.merge(df_buildings, on=join_cols)
    return filter_by_country(df, country)