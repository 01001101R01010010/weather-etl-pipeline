import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from extract import extract_all_cities
from transform import transform_weather_data
from load import init_database, load_to_duckdb
from datetime import datetime

def run_pipeline():
    print(f"\n=== Pipeline start: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

    print("\n[1/3] Ekstrakcja danych z API...")
    raw_data = extract_all_cities()

    if not raw_data:
        print("Brak danych — pipeline przerwany.")
        return

    print(f"\n[2/3] Transformacja {len(raw_data)} rekordów...")
    df = transform_weather_data(raw_data)

    print(f"\n[3/3] Ładowanie do DuckDB...")
    init_database()
    load_to_duckdb(df)

    print("\n=== Pipeline zakończony ===\n")

if __name__ == "__main__":
    run_pipeline()