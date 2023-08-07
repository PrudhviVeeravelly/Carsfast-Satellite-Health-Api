# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import requests
import datetime
import time

app = Flask(__name__)

# Global variables to store the satellite data
satellite_data_5min = []
satellite_data_1min = []
last_warning_time = None

# Helper function to fetch satellite data from the API
def fetch_satellite_data():
    url = "https://api.cfast.dev/satellite/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_previous_5min_data():
    global satellite_data_5min  # Add the global keyword here

    # Remove old data (older than 5 minutes)
    five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)
    satellite_data_5min = [d for d in satellite_data_5min if datetime.datetime.fromisoformat(d['last_updated']) >= five_minutes_ago]

    # Fetch the latest satellite data
    data = fetch_satellite_data()
    if data:
        satellite_data_5min.append(data)

    return satellite_data_5min

def fetch_previous_1min_data():
    global satellite_data_1min  # Add the global keyword here

    # Remove old data (older than 1 minute)
    one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
    satellite_data_1min = [d for d in satellite_data_1min if datetime.datetime.fromisoformat(d['last_updated']) >= one_minute_ago]

    # Fetch the latest satellite data
    data = fetch_satellite_data()
    if data:
        satellite_data_1min.append(data)

    return satellite_data_1min


# Health logic
def check_health(prev_1min_data):

    global last_warning_time 

    # Default value for avg_altitude when prev_1min_data is empty
    avg_altitude = 0.0

    if len(prev_1min_data) > 0:
        altitudes = [float(d['altitude']) for d in prev_1min_data]
        avg_altitude = sum(altitudes) / len(altitudes)
        
    # Check for altitude warning
    if avg_altitude < 160 and (not last_warning_time or time.time() - last_warning_time > 60):
        last_warning_time = time.time()
        return "WARNING: RAPID ORBITAL DECAY IMMINENT"
    elif avg_altitude >= 160 and last_warning_time:
        last_warning_time = None
        return "Sustained Low Earth Orbit Resumed"
    else:
        return "Altitude is A-OK"

#Stats logic
def check_stats(prev_5min_data):

    # Calculate stats for the last 5 minutes
    if len(satellite_data_5min) > 0:
        altitudes = [float(d['altitude']) for d in prev_5min_data]
        min_altitude = min(altitudes)
        max_altitude = max(altitudes)
        avg_altitude = sum(altitudes) / len(altitudes)
    
        return f"Min={min_altitude:.3f} km, Max={max_altitude:.3f} km, Avg={avg_altitude:.3f} km"
        
    else:
        return "No data available for the last 5 minutes"
        

# Route to get stats
@app.route('/stats')
def get_stats():
    prev_5min_data = fetch_previous_5min_data()
    return jsonify(check_stats(prev_5min_data))

# Route to get health status
@app.route('/health')
def get_health():
    prev_1min_data = fetch_previous_1min_data()
    return jsonify(check_health(prev_1min_data))

if __name__ == '__main__':
    app.run(debug=True)
