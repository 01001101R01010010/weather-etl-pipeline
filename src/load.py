import duckdb
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/weather.duckdb")

def init_database():
    DB_PATH.parent.mkdir(exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    con.execute("""
        CREATE TABLE IF NOT EXISTS weather_readings (
            city            VARCHAR,
            country         VARCHAR,
            fetched_at      TIMESTAMP,
            temp_c          FLOAT,
            feels_like_c    FLOAT,
            temp_min_c      FLOAT,
            temp_max_c      FLOAT,
            humidity_pct    INTEGER,
            pressure_hpa    INTEGER,
            wind_speed_ms   FLOAT,
            wind_deg        INTEGER,
            cloudiness_pct  INTEGER,
            weather_main    VARCHAR,
            weather_desc    VARCHAR,
            visibility_km   FLOAT,
            temp_category   VARCHAR
        )
    """)
    con.close()

def load_to_duckdb(df: pd.DataFrame):
    con = duckdb.connect(str(DB_PATH))
    con.execute("INSERT INTO weather_readings SELECT * FROM df")
    rows = con.execute("SELECT COUNT(*) FROM weather_readings").fetchone()[0]
    print(f"✓ Zapisano {len(df)} rekordów. Łącznie w bazie: {rows}")
    con.close()

def query_latest() -> pd.DataFrame:
    con = duckdb.connect(str(DB_PATH))
    df = con.execute("""
        SELECT * FROM weather_readings
        QUALIFY ROW_NUMBER() OVER (
            PARTITION BY city ORDER BY fetched_at DESC
        ) = 1
    """).df()
    con.close()
    return df