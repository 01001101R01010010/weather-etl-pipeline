import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path

DB_PATH = Path("data/weather.duckdb")

st.set_page_config(
    page_title="Weather ETL Dashboard",
    page_icon="⛅",
    layout="wide"
)

@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    con = duckdb.connect(str(DB_PATH), read_only=True)
    df = con.execute("""
        SELECT * FROM weather_readings
        ORDER BY fetched_at DESC
    """).df()
    con.close()
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])
    return df

df = load_data()

st.title("Weather ETL Dashboard")
st.caption(f"Ostatnia aktualizacja: {df['fetched_at'].max().strftime('%Y-%m-%d %H:%M')} UTC")

latest = df.sort_values("fetched_at").groupby("city").last().reset_index()
cols = st.columns(len(latest))
for col, (_, row) in zip(cols, latest.iterrows()):
    col.metric(
        label=row["city"],
        value=f"{row['temp_c']:.1f} °C",
        delta=row["weather_desc"]
    )

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Temperatura w czasie")
    city_filter = st.multiselect(
        "Wybierz miasta",
        options=df["city"].unique(),
        default=list(df["city"].unique())
    )
    filtered = df[df["city"].isin(city_filter)]
    fig = px.line(
        filtered,
        x="fetched_at", y="temp_c",
        color="city",
        labels={"temp_c": "Temperatura (°C)", "fetched_at": "Czas"},
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Wilgotność vs temperatura")
    fig2 = px.scatter(
        latest,
        x="temp_c", y="humidity_pct",
        color="city", size="wind_speed_ms",
        text="city",
        labels={
            "temp_c": "Temperatura (°C)",
            "humidity_pct": "Wilgotność (%)",
            "wind_speed_ms": "Wiatr (m/s)"
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Surowe dane")
st.dataframe(latest[[
    "city", "temp_c", "feels_like_c", "humidity_pct",
    "wind_speed_ms", "weather_desc", "fetched_at"
]], use_container_width=True)