import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#94a3b8",
    margin=dict(l=0, r=40, t=10, b=10),
)


def bar_density(df: pd.DataFrame, top_n: int) -> go.Figure:
    df_sorted = df.sort_values("urban_density_score").tail(top_n)
    fig = px.bar(
        df_sorted,
        x="urban_density_score",
        y="city",
        orientation="h",
        color="urban_density_score",
        color_continuous_scale="Blues",
        labels={"urban_density_score": "Score", "city": ""},
        text=df_sorted["urban_density_score"].round(3),
    )
    fig.update_traces(textposition="outside", textfont_size=10)
    fig.update_layout(
        **LAYOUT_BASE,
        coloraxis_showscale=False,
        height=400,
        xaxis=dict(gridcolor="#1e293b", showgrid=True),
        yaxis=dict(gridcolor="rgba(0,0,0,0)"),
    )
    return fig


def radar_composition(df: pd.DataFrame, top_n: int = 5) -> go.Figure:
    fig = go.Figure()
    for _, row in df.head(top_n).iterrows():
        total = row["num_buildings"] + row["num_amenities"] + row["num_roads"]
        if total == 0:
            continue
        fig.add_trace(go.Scatterpolar(
            r=[
                row["num_buildings"] / total,
                row["num_amenities"] / total,
                row["num_roads"] / total,
            ],
            theta=["Bâtiments", "Équipements", "Routes"],
            fill="toself",
            name=row["city"],
            opacity=0.7,
        ))
    fig.update_layout(
        **{k: v for k, v in LAYOUT_BASE.items() if k != "margin"},
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, gridcolor="#1e293b", color="#475569"),
            angularaxis=dict(gridcolor="#1e293b", color="#94a3b8"),
        ),
        legend=dict(font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
    )
    return fig


def scatter_buildings_amenities(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        x="num_buildings",
        y="num_amenities",
        hover_name="city",
        color="num_amenities",
        color_continuous_scale="Teal",
        size="num_amenities",
        size_max=30,
        labels={"num_buildings": "Bâtiments", "num_amenities": "Équipements"},
    )
    fig.update_layout(
        **LAYOUT_BASE,
        coloraxis_showscale=False,
        height=350,
        xaxis=dict(gridcolor="#1e293b"),
        yaxis=dict(gridcolor="#1e293b"),
    )
    return fig