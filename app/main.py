from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.db import fetch_latest_data, store_data
from app.routes.api import router as api_router  # Import the API router
import os
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine the environment
ENV = os.getenv("ENV")
if not ENV:
    raise ValueError("ENV variable is not set in the .env file!")

# Dynamically import sensor methods based on the environment
if ENV == "development":
    print("Using simulated sensor data (development mode).")
    from app.sensor_dev import read_sensors, control_led, control_pump
else:
    print("Using real sensor data (production mode).")
    try:
        from app.sensors import read_sensors, control_led, control_pump
    except ImportError as e:
        raise ImportError(f"Error importing real sensor modules: {e}")

# Initialize FastAPI app
app = FastAPI()

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="app/templates")

# Serve static files for CSS, JavaScript, etc.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include the API router for additional endpoints
app.include_router(api_router)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the SmartGarden Dashboard."""
    # Fetch the latest sensor data
    data = fetch_latest_data()
    print(f"Fetched data for dashboard: {data}")  # Debugging

    if data:
        context = {
            "request": request,
            "data": {
                "temperature": data[2],
                "humidity": data[3],
                "pressure": data[4],
                "soil_moisture": data[7],
                "luminosity": data[6]
            }
        }
    else:
        context = {
            "request": request,
            "data": {
                "temperature": "N/A",
                "humidity": "N/A",
                "soil_moisture": "N/A",
                "luminosity": "N/A"
            }
        }
    return templates.TemplateResponse("index.html", context)

def main_loop():
    """Store sensor data in the database based on the environment."""
    while True:
        try:
            # Step 1: Generate sensor values (real or simulated based on ENV)
            data = read_sensors()

            # Step 2: Store the data in the database
            store_data(data)

            # Step 3: Print data to console (for debugging)
            print(f"Stored data: {data}")

            # Delay for sensor readings
            time.sleep(60)
        except Exception as e:
            print(f"Error in sensor loop: {e}")
            break

# Start the sensor loop in a background thread
@app.on_event("startup")
def start_background_task():
    threading.Thread(target=main_loop, daemon=True).start()
    print("Sensor loop started in background thread.")
