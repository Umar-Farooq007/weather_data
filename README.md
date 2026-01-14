🌦️ Real-Time Weather & Events Tracker (MySQL + Python)

This project demonstrates a basic ETL pipeline using Python, MySQL, Pandas, and Matplotlib.
It loads event data from a CSV file, stores it in MySQL, and generates analytical graphs comparing Low Risk vs High Risk weather events.

📂 Project Structure
weather_data/
│
├── data/
│   └── events.csv
│
├── etl.py
├── graphs.py
├── schema.sql
├── README.md
└── weather_api/   (virtual environment)

🛠️ Tech Stack

Python 3.10+

MySQL 8.0

Pandas

PyMySQL

Matplotlib

⚙️ Environment Setup (INIT COMMANDS)
1️⃣ Create Virtual Environment
python -m venv weather_api

2️⃣ Activate Virtual Environment

Windows

weather_api\Scripts\activate


Linux / Mac

source weather_api/bin/activate

📦 Install Required Libraries
pip install pymysql pandas matplotlib

🗄️ MySQL Database Setup
1️⃣ Login to MySQL
mysql -u root -p

2️⃣ Run Schema File
SOURCE schema.sql;


✅ This creates:

Database: weather_events_db

Table: events_weather

📄 Sample CSV Format (data/events.csv)
event_name,venue,city,event_date,temperature,rain,snow,weather_risk
Music Fest,Open Ground,Bangalore,2025-01-10,32,0,0,Low Risk
Cricket Match,Stadium,Chennai,2025-01-12,36,10,0,High Risk

🔄 Run ETL Pipeline
Load CSV → MySQL
python etl.py


✔ Reads events.csv
✔ Inserts data into events_weather table

📊 Generate Graphs & Analytics
python graphs.py

Graphs Included:

High Risk Events by Venue

Average Temperature by City

Weather Risk Distribution (Pie)

High vs Low Risk by City

High vs Low Risk by Venue (Stacked)

Average Temperature by Weather Risk

❗ Common Errors & Fixes
🔴 Error: Unknown database
Unknown database 'weather_events'


✅ Fix: Ensure DB name is weather_events_db in both MySQL & Python

🔴 Error: File not found
No such file or directory: 'data/events.csv'


✅ Fix:

mkdir data


Move events.csv inside data/

🔴 Pandas SQL Warning
pandas only supports SQLAlchemy...
Explanation (Short)

“This project demonstrates an ETL workflow where event data is extracted from CSV, transformed using Pandas, loaded into MySQL, and analyzed using multiple visualizations comparing high-risk and low-risk weather events.”
+--------------------------------------------------+
|                  events_weather                  |
+--------------------------------------------------+
| PK  event_id                                     |
|     event_name                                   |
|     venue                                        |
|     city                                         |
|     event_date                                   |
|     temperature                                  |
|     rain                                         |
|     snow                                         |
|     weather_risk                                 |
|     created_at                                   |
+--------------------------------------------------+
