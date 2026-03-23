import pandas as pd
from datetime import datetime, timezone

def transform_weather_data(raw_data: list[dict]) -> pd.DataFrame:
    records = []

    for item in raw_data:
        record = {
            "city":            item["name"],
            "country":         item["sys"]["country"],
            "fetched_at":      datetime.now(timezone.utc).isoformat(),

            "temp_c":          round(item["main"]["temp"], 1),
            "feels_like_c":    round(item["main"]["feels_like"], 1),
            "temp_min_c":      round(item["main"]["temp_min"], 1),
            "temp_max_c":      round(item["main"]["temp_max"], 1),

            "humidity_pct":    item["main"]["humidity"],
            "pressure_hpa":    item["main"]["pressure"],
            "wind_speed_ms":   item["wind"]["speed"],
            "wind_deg":        item["wind"].get("deg", None),
            "cloudiness_pct":  item["clouds"]["all"],

            "weather_main":    item["weather"][0]["main"],
            "weather_desc":    item["weather"][0]["description"],

            "visibility_km":   round(item.get("visibility", 0) / 1000, 1),
        }
        records.append(record)

    df = pd.DataFrame(records)
    df = df.dropna(subset=["temp_c"])

    df["temp_category"] = pd.cut(
        df["temp_c"],
        bins=[-50, 0, 10, 20, 30, 50],
        labels=["mróz", "zimno", "chłodno", "ciepło", "gorąco"]
    )

    return df