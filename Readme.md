# Satellite Health API

This web application monitors the health status of the satellite launched by Carsfast.

## Setup and Run

1. Clone the repository:
   ```bash
   git clone https://github.com/PrudhviVeeravelly/satellite-health-api.git

2. Navigate to the project directory:

cd satellite-health-api

3. Install the required dependencies:

pip install requirements.txt

4. Start the application:

python3 app.py

5. The API will now be accessible at http://127.0.0.1:5000/.

For stats - http://127.0.0.1:5000/stats
For health - http://127.0.0.1:5000/health

## API Endpoints

GET /stats
Returns the minimum, maximum, and average altitude for the last 5 minutes. If there is no data available for 5 minutes, it will return the stats for what is available.

GET /health
Monitors the health status of the satellite. It returns one of the following messages:

"WARNING: RAPID ORBITAL DECAY IMMINENT" when the average altitude over the last minute goes below 160 km.
"Sustained Low Earth Orbit Resumed" for 1 minute once the average altitude is 160 km or above again.
"Altitude is A-OK" when the average altitude is above 160 km and there is no rapid orbital decay warning.


## Unit Tests
Run the unit tests to check the health logic:

python -m unittest test_app.py
