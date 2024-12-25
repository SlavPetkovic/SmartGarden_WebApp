import os
from dotenv import load_dotenv
from app.db import store_data
import time
import threading

# Load environment variables from .env file
load_dotenv()

# Get the environment setting from .env
ENV = os.getenv("ENV")
if not ENV:
    raise ValueError("ENV variable is not set in the .env file!")
else:
    print(f"Loaded ENV: {ENV}")  # Debugging

# Define main_loop conditionally based on ENV
if ENV.strip().lower() == "development":
    print("Running in development mode: Simulated sensor data.")
    from app.sensor_dev import read_sensors, control_led, control_pump

    def main_loop():
        while True:
            try:
                data = read_sensors()
                store_data(data)
                print(f"Stored simulated data: {data}")
                time.sleep(1)
            except Exception as e:
                print(f"Error in simulated loop: {e}")
                break

elif ENV.strip().lower() == "production":
    try:
        print("Running in production mode: Real sensor data.")
        import board
        from busio import I2C
        import adafruit_bme680
        import adafruit_veml7700
        from adafruit_seesaw.seesaw import Seesaw
        import RPi.GPIO as GPIO
        import atexit
        import datetime

        print("Successfully imported Raspberry Pi sensor libraries.")

        # GPIO setup
        rc1 = 24
        rc2 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rc1, GPIO.OUT)
        GPIO.setup(rc2, GPIO.OUT)
        GPIO.output(rc1, False)
        GPIO.output(rc2, False)

        def cleanup_gpio():
            GPIO.cleanup()

        atexit.register(cleanup_gpio)

        i2c = board.I2C()
        veml7700 = adafruit_veml7700.VEML7700(i2c)
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        ss = Seesaw(i2c, addr=0x36)

        def read_sensors():
            timestamp = datetime.datetime.now()
            temperature = round(bme680.temperature, 2)
            humidity = round(bme680.humidity, 2)
            pressure = round(bme680.pressure, 2)
            luminosity = round(veml7700.light, 2)
            soil_moisture = round(ss.moisture_read(), 2)
            return timestamp, temperature, humidity, pressure, luminosity, soil_moisture

        def main_loop():
            while True:
                try:
                    data = read_sensors()
                    store_data(data)
                    print(f"Stored real sensor data: {data}")
                    time.sleep(1)
                except Exception as e:
                    print(f"Error in production loop: {e}")
                    break

    except ImportError as e:
        print(f"Critical ImportError: {e}")
        print("Raspberry Pi-specific libraries are required for production mode.")
        raise e
else:
    print(f"Invalid ENV: {ENV}. Terminating application.")
    raise ValueError("ENV must be 'development' or 'production'.")

if __name__ == "__main__":
    # Start the appropriate main_loop based on the environment
    threading.Thread(target=main_loop, daemon=True).start()
    print("Sensor loop started in background thread.")
    while True:
        time.sleep(1)
