import streamlit as st
from utils.data import load_all, filter_by_country, merge_amenities_buildings
from utils.charts import bar_density, radar_composition, scatter_buildings_amenities
from utils.components import load_css, section_title, kpi_row, data_table, sidebar, footer

st.set_page_config(
    page_title="Urban Analytics OSM",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# --- DATA ---
df_density, df_amenities, df_buildings = load_all()

# --- SIDEBAR ---
selected_country, top_n = sidebar(df_density)

# --- FILTRES ---
df_filtered = filter_by_country(df_density, selected_country)
df_top      = df_filtered.sort_values("urban_density_score", ascending=False).head(top_n)
df_merge    = merge_amenities_buildings(df_amenities, df_buildings, selected_country)

# --- HEADER ---
pays_label = "Monde entier" if selected_country == "Tous" else selected_country
st.markdown("# OSM Urban Analytics")
st.markdown(f"<div style='color:#475569;margin-bottom:2rem'>Analyse de la densité urbaine • {pays_label}</div>", unsafe_allow_html=True)

# --- KPIs ---
kpi_row(df_filtered)
st.markdown("<br>", unsafe_allow_html=True)

# --- LIGNE 1 : Bar + Radar ---
col_left, col_right = st.columns([3, 2])

with col_left:
    section_title(f"Top {top_n} — Score de densité urbaine")
    st.plotly_chart(bar_density(df_top, top_n), use_container_width=True)

with col_right:
    section_title("Composition — Buildings / Amenities / Roads")
    st.plotly_chart(radar_composition(df_top), use_container_width=True)

# --- LIGNE 2 : Scatter + Table ---
col_left2, col_right2 = st.columns([2, 3])

with col_left2:
    section_title("Buildings vs Amenities")
    st.plotly_chart(scatter_buildings_amenities(df_merge), use_container_width=True)

with col_right2:
    section_title(f"Données détaillées — Top {top_n}")
    data_table(df_top, top_n)

# --- FOOTER ---
footer()