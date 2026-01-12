-- =========================================================
-- Real-Time Weather & Events Tracker
-- Database: MySQL
-- =========================================================

-- Create database
CREATE DATABASE IF NOT EXISTS weather_events_db;
USE weather_events_db;

-- Drop table if exists (for reruns)
DROP TABLE IF EXISTS events_weather;

-- Create table
CREATE TABLE events_weather (
    event_id INT AUTO_INCREMENT PRIMARY KEY,

    event_name VARCHAR(255) NOT NULL,
    venue VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,

    temperature DECIMAL(5,2),
    rain DECIMAL(5,2) DEFAULT 0,
    snow DECIMAL(5,2) DEFAULT 0,

    weather_risk ENUM('Low Risk', 'High Risk') NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Prevent duplicate events at same venue on same date
    UNIQUE KEY uniq_event (event_name, venue, event_date),

    -- Data integrity constraints
    CHECK (temperature BETWEEN -50 AND 60),
    CHECK (rain >= 0),
    CHECK (snow >= 0)
);

-- Indexes for analytics performance
CREATE INDEX idx_city_date ON events_weather (city, event_date);
CREATE INDEX idx_weather_risk ON events_weather (weather_risk);
