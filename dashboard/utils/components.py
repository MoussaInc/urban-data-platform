import streamlit as st
import pandas as pd
from pathlib import Path


def load_css() -> None:
    css_path = Path(__file__).parent.parent / "style.css"
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def section_title(label: str) -> None:
    st.markdown(f"<div class='section-title'>{label}</div>", unsafe_allow_html=True)


def kpi_card(col, value: str, label: str) -> None:
    col.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-value'>{value}</div>
            <div class='kpi-label'>{label}</div>
        </div>
    """, unsafe_allow_html=True)


def kpi_row(df: pd.DataFrame) -> None:
    col1, col2, col3, col4 = st.columns(4)
    kpi_card(col1, str(len(df)), "Villes analysées")
    kpi_card(col2, str(round(df["urban_density_score"].mean(), 3)), "Score moyen")
    kpi_card(col3, f"{int(df['num_buildings'].sum()):,}", "Bâtiments total")
    kpi_card(col4, f"{int(df['num_amenities'].sum()):,}", "Équipements total")


def data_table(df: pd.DataFrame, top_n: int) -> None:
    df_display = (
        df[["city", "country", "num_buildings", "num_amenities", "num_roads", "urban_density_score"]]
        .head(top_n)
        .copy()
    )
    df_display.columns = ["Ville", "Pays", "Bâtiments", "Équipements", "Routes", "Score"]
    df_display["Score"] = df_display["Score"].round(4)
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=350,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score", min_value=0, max_value=1, format="%.4f"
            ),
            "Bâtiments":   st.column_config.NumberColumn(format="%d"),
            "Équipements": st.column_config.NumberColumn(format="%d"),
            "Routes":      st.column_config.NumberColumn(format="%d"),
        },
    )


def sidebar(df_density: pd.DataFrame) -> tuple[str, int]:
    with st.sidebar:
        st.markdown("## 🏙️ Urban Analytics")
        st.markdown("---")
        countries = sorted(df_density["country"].dropna().unique())
        selected_country = st.selectbox("Pays", ["Tous"] + list(countries))
        top_n = st.slider("Top N villes", min_value=5, max_value=30, value=10)
        st.markdown("---")
        st.markdown(
            f"<div style='color:#475569;font-size:0.75rem'>"
            f"Source: OpenStreetMap<br>{len(df_density)} villes analysées</div>",
            unsafe_allow_html=True,
        )
    return selected_country, top_n


def footer() -> None:
    st.markdown("---")
    st.markdown(
        "<div class='footer'>Urban Data Platform • OpenStreetMap Analytics • dbt + BigQuery + Airflow</div>",
        unsafe_allow_html=True,
    )