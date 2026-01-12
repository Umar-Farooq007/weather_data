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
    port=3306,
    database="weather_events_db"   # MUST match schema.sql
)

cursor = connector.cursor()
print("MySQL connection successful")

# =========================================================
# City → Latitude & Longitude Mapping
# =========================================================

CITY_COORDS = {
    "Bangalore": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707)
}

# =========================================================
# Weather API Function (Open-Meteo)
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
# Read CSV File
# =========================================================

file_path = "data/events.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"CSV file not found at: {file_path}")

events_df = pd.read_csv(file_path)
print("CSV file loaded successfully")

# =========================================================
# Insert Query
# =========================================================

insert_sql = """
INSERT INTO events_weather
(event_name, venue, city, event_date, temperature, rain, snow, weather_risk)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# =========================================================
# ETL Process
# =========================================================

for _, row in events_df.iterrows():
    try:
        event_name = row["Event Name"]
        venue = row["Venue"]
        city = row["City"]
        event_date = pd.to_datetime(row["Date"]).strftime("%Y-%m-%d")

        if city not in CITY_COORDS:
            print(f"City not supported: {city}")
            continue

        temperature, rain, snow = get_weather(city, event_date)

        weather_risk = "High Risk" if rain > 0 or snow > 0 else "Low Risk"

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
        print(f"Inserted: {event_name} | {city} | {event_date}")

    except pymysql.err.IntegrityError:
        print(f"Duplicate skipped: {event_name} | {event_date}")

    except Exception as e:
        print(f"Error processing {event_name}: {e}")

# =========================================================
# Close Connection
# =========================================================

cursor.close()
connector.close()
print("ETL process completed successfully")
