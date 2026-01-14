import pymysql
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# MySQL Connection
# =========================================================

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="weather_events_db",
    port=3306
)

print("MySQL connection successful")

# =========================================================
# Load Data
# =========================================================

query = "SELECT * FROM events_weather"
df = pd.read_sql(query, connection)
connection.close()

print("Data loaded")
print(df[["event_name", "city", "weather_risk"]].head())

if df.empty:
    print("No data found. Run etl.py first.")
    exit()

# =========================================================
# GRAPH 1: High vs Low Risk Count
# =========================================================

risk_counts = df["weather_risk"].value_counts()

plt.figure()
plt.bar(risk_counts.index, risk_counts.values)
plt.title("High Risk vs Low Risk Events")
plt.xlabel("Weather Risk")
plt.ylabel("Number of Events")
plt.tight_layout()
plt.show()

# =========================================================
# GRAPH 2: Weather Risk Distribution (PIE)
# =========================================================

plt.figure()
plt.pie(
    risk_counts.values,
    labels=risk_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Weather Risk Distribution")
plt.axis("equal")
plt.show()

# =========================================================
# GRAPH 3: City-wise High vs Low Risk
# =========================================================

city_risk = (
    df.groupby(["city", "weather_risk"])
    .size()
    .unstack(fill_value=0)
)

plt.figure()
city_risk.plot(kind="bar")
plt.title("City-wise High vs Low Risk Events")
plt.xlabel("City")
plt.ylabel("Number of Events")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# =========================================================
# GRAPH 4: Venue-wise High vs Low Risk (Top 6)
# =========================================================

venue_risk = (
    df.groupby(["venue", "weather_risk"])
    .size()
    .unstack(fill_value=0)
)

top_venues = venue_risk.sum(axis=1).sort_values(ascending=False).head(6)
venue_risk_top = venue_risk.loc[top_venues.index]

plt.figure()
venue_risk_top.plot(kind="bar")
plt.title("Venue-wise High vs Low Risk Events")
plt.xlabel("Venue")
plt.ylabel("Number of Events")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

print("Graphs generated successfully")
