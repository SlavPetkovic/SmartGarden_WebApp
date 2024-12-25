import random
import datetime

def read_sensors():
    """Simulate reading sensors by generating random values."""
    print("Generating random sensor values...")  # Debugging
    timestamp = datetime.datetime.now()
    temperature = round(random.uniform(15.0, 30.0), 2)  # Simulate temperature in Celsius
    gas = round(random.uniform(0, 500), 2)  # Simulate gas resistance
    humidity = round(random.uniform(30.0, 70.0), 2)  # Simulate humidity percentage
    pressure = round(random.uniform(950.0, 1050.0), 2)  # Simulate pressure in hPa
    altitude = round(random.uniform(0, 500), 2)  # Simulate altitude in meters
    luminosity = round(random.uniform(0, 1000), 2)  # Simulate luminosity in lux
    soil_moisture = round(random.uniform(200, 800), 2)  # Simulate soil moisture
    soil_temperature = round(random.uniform(10.0, 25.0), 2)  # Simulate soil temperature
    return timestamp, temperature, gas, humidity, pressure, altitude, luminosity, soil_moisture, soil_temperature

def control_led(luminosity):
    """Simulate controlling the LED based on luminosity."""
    print(f"Simulated: Controlling LED. Luminosity = {luminosity}")
    if luminosity >= 100:
        print("Simulated: Lights are OFF")
    else:
        print("Simulated: Lights are ON")

def control_pump(soil_moisture):
    """Simulate controlling the pump based on soil moisture."""
    print(f"Simulated: Controlling Pump. Soil Moisture = {soil_moisture}")
    if soil_moisture <= 400:
        print("Simulated: Pump is OFF")
    else:
        print("Simulated: Pump is ON")
