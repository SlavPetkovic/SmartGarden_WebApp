from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.db import fetch_latest_data, store_data
from app.sensor_dev import read_sensors  # Use `sensor_dev` for simulated data
from app.routes.api import router as api_router  # Import the API router
import threading
import time

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
    """Simulate storing random sensor data in the database."""
    while True:
        try:
            # Step 1: Generate random sensor values
            data = read_sensors()

            # Step 2: Store the simulated data in the database
            store_data(data)

            # Step 3: Print data to console (for debugging)
            print(f"Stored simulated data: {data}")

            # Delay for simulation
            time.sleep(1)  # Simulate a 1-second interval between readings
        except Exception as e:
            print(f"Error in simulated loop: {e}")
            break

# Start the sensor loop in a background thread
@app.on_event("startup")
def start_background_task():
    threading.Thread(target=main_loop, daemon=True).start()
    print("Sensor loop started in background thread.")
