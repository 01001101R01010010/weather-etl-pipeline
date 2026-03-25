# Weather ETL Pipeline

Automated hourly ETL pipeline that collects weather data for 5 major Polish cities, transforms it with Python, stores it in DuckDB, and visualizes it in an interactive Streamlit dashboard.

## Architecture
```
OpenWeatherMap API → Python ETL → DuckDB → Streamlit Dashboard
                                     ↑
                              GitHub Actions (every hour)
```

## Tech Stack

| Layer | Tool |
|---|---|
| Extract | Python `requests`, OpenWeatherMap API |
| Transform | `pandas` — cleaning, validation, categorization |
| Load | `DuckDB` — columnar database, no server needed |
| Orchestration | GitHub Actions (cron every 1h) |
| Visualization | Streamlit + Plotly |

## Features

- Collects real-time weather data for Warsaw, Krakow, Gdansk, Wroclaw and Poznan
- Runs automatically every hour via GitHub Actions
- Stores historical data in DuckDB for trend analysis
- Interactive dashboard with temperature trends and humidity charts

## Project Structure
```
weather-etl-pipeline/
├── .github/workflows/etl.yml   # GitHub Actions automation
├── src/
│   ├── extract.py              # Fetch data from API
│   ├── transform.py            # Clean and normalize data
│   ├── load.py                 # Save to DuckDB
│   └── pipeline.py             # Orchestrate ETL steps
├── dashboard/
│   └── app.py                  # Streamlit dashboard
├── data/
│   └── weather.duckdb          # Local database
└── requirements.txt
```

## Run Locally
```bash
git clone https://github.com/01001101R01010010/weather-etl-pipeline.git
cd weather-etl-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "OPENWEATHER_API_KEY=your_key_here" > .env
python3 src/pipeline.py
streamlit run dashboard/app.py
```

## Data Schema

| Column | Type | Description |
|---|---|---|
| city | VARCHAR | City name |
| temp_c | FLOAT | Temperature in °C |
| humidity_pct | INTEGER | Humidity in % |
| wind_speed_ms | FLOAT | Wind speed in m/s |
| weather_desc | VARCHAR | Weather description |
| fetched_at | TIMESTAMP | Fetch time (UTC) |