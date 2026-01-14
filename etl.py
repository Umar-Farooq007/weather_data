import pandas as pd
import requests
import pymysql
import os

# =========================================================
# MySQL Connection
# =========================================================

connector = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="weather_events_db",
    port=3306
)

cursor = connector.cursor()
print("MySQL connection successful")

# =========================================================
# City → Latitude & Longitude
# =========================================================

CITY_COORDS = {
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707)
}

# =========================================================
# Weather API (Open-Meteo)
# =========================================================

def get_weather(city, date):
    lat, lon = CITY_COORDS[city]

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,rain_sum,snowfall_sum"
        f"&start_date={date}&end_date={date}"
        f"&timezone=auto"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    temperature = data["daily"]["temperature_2m_max"][0]
    rain = data["daily"]["rain_sum"][0]
    snow = data["daily"]["snowfall_sum"][0]

    return temperature, rain, snow

# =========================================================
# Read CSV
# =========================================================

file_path = "data/events.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"CSV not found: {file_path}")

events_df = pd.read_csv(file_path)
print("CSV file loaded successfully")
print(events_df.head())

# =========================================================
# Insert SQL
# =========================================================

insert_sql = """
INSERT INTO events_weather
(event_name, venue, city, event_date, temperature, rain, snow, weather_risk)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# =========================================================
# ETL PROCESS
# =========================================================

outdoor_keywords = ["Outdoor", "Open", "Street", "Marathon", "Festival"]

for _, row in events_df.iterrows():
    event_name = None

    try:
        event_name = row["event_name"]
        venue = row["venue"]
        city = row["city"]
        event_date = pd.to_datetime(row["event_date"]).strftime("%Y-%m-%d")

        if city not in CITY_COORDS:
            print(f"Unsupported city: {city}")
            continue

        temperature, rain, snow = get_weather(city, event_date)

        # Business logic for weather risk
        is_outdoor = any(word.lower() in event_name.lower() for word in outdoor_keywords)

        if rain >= 5 or snow > 0 or (is_outdoor and temperature >= 32):
            weather_risk = "High Risk"
        else:
            weather_risk = "Low Risk"

        cursor.execute(
            insert_sql,
            (
                event_name,
                venue,
                city,
                event_date,
                temperature,
                rain,
                snow,
                weather_risk
            )
        )

        connector.commit()
        print(f"Inserted: {event_name} | {weather_risk}")

    except pymysql.err.IntegrityError:
        print(f"Duplicate skipped: {event_name}")

    except Exception as e:
        print(f"Error processing row: {e}")

# =========================================================
# Close Connection
# =========================================================

cursor.close()
connector.close()
print("ETL process completed successfully")
