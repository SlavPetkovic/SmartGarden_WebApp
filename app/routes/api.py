from fastapi import APIRouter
from app.sensors import read_sensors, control_led, control_pump
from app.db import fetch_latest_data, store_data

router = APIRouter()

@router.get("/sensors/latest")
async def get_latest_data():
    """Fetch the latest sensor data."""
    data = fetch_latest_data()
    if data:
        return {
            "timestamp": data[1],
            "temperature": data[2],
            "gas": data[3],
            "humidity": data[4],
            "pressure": data[5],
            "altitude": data[6],
            "luminosity": data[7],
            "soil_moisture": data[8],
            "soil_temperature": data[9],
        }
    return {"error": "No data found"}

@router.post("/control/lights")
async def api_control_lights(on: bool):
    """API endpoint to control lights."""
    control_led(100 if on else 0)
    return {"lights": "on" if on else "off"}

@router.post("/control/pump")
async def api_control_pump(on: bool):
    """API endpoint to control pump."""
    control_pump(0 if on else 500)
    return {"pump": "on" if on else "off"}

@router.post("/simulate")
async def simulate_sensor_reading():
    """Simulate a sensor reading and store it in the database."""
    data = read_sensors()
    store_data(data)
    return {"message": "Simulated data stored", "data": data}
