import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

print("Data loaded into DataFrame")
print(df.head())

# =========================================================
# GRAPH 1: High Risk Events by Venue
# =========================================================
high_risk_df = df[df["weather_risk"] == "High Risk"]

if high_risk_df.empty:
    print("⚠️ No High Risk events found. Skipping Graph 1.")
else:
    venue_counts = high_risk_df["venue"].value_counts()
    plt.figure()
    plt.bar(venue_counts.index, venue_counts.values, color='red')
    plt.title("High Risk Weather Events by Venue")
    plt.xlabel("Venue")
    plt.ylabel("Number of High Risk Events")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# =========================================================
# GRAPH 2: Average Temperature by City
# =========================================================
avg_temp_city = df.groupby("city")["temperature"].mean()
plt.figure()
plt.bar(avg_temp_city.index, avg_temp_city.values, color='skyblue')
plt.title("Average Temperature by City")
plt.xlabel("City")
plt.ylabel("Temperature (°C)")
plt.tight_layout()
plt.show()

# =========================================================
# GRAPH 3: Weather Risk Distribution
# =========================================================
risk_counts = df["weather_risk"].value_counts()
plt.figure()
plt.pie(
    risk_counts.values,
    labels=risk_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=['green', 'red']
)
plt.title("Weather Risk Distribution")
plt.axis("equal")
plt.show()

# =========================================================
# GRAPH 4: High vs Low Risk Count by City (Side-by-Side)
# =========================================================
risk_city = df.groupby(["city", "weather_risk"]).size().unstack(fill_value=0)
risk_city.plot(kind='bar', figsize=(8,5))
plt.title("High vs Low Risk Events by City")
plt.xlabel("City")
plt.ylabel("Number of Events")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# =========================================================
# GRAPH 5: Average Temperature by Weather Risk
# =========================================================
avg_temp_risk = df.groupby("weather_risk")["temperature"].mean()
plt.figure()
plt.bar(avg_temp_risk.index, avg_temp_risk.values, color=['green','red'])
plt.title("Average Temperature by Weather Risk")
plt.xlabel("Weather Risk")
plt.ylabel("Average Temperature (°C)")
plt.tight_layout()
plt.show()

# =========================================================
# GRAPH 6: High vs Low Risk by Venue (Stacked)
# =========================================================
risk_venue = df.groupby(["venue", "weather_risk"]).size().unstack(fill_value=0)
risk_venue.plot(kind='bar', stacked=True, figsize=(10,5))
plt.title("High vs Low Risk Events by Venue (Stacked)")
plt.xlabel("Venue")
plt.ylabel("Number of Events")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
