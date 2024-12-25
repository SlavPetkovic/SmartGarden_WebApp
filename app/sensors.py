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

# Use `sensor_dev.py` if in development mode
if ENV == "development":
    print("Using simulated sensor data (development mode).")
    from app.sensor_dev import read_sensors, control_led, control_pump

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

else:
    # Production logic with real sensors
    try:
        print("Using real sensor data (production mode).")
        import board
        from busio import I2C
        import adafruit_bme680
        import adafruit_veml7700
        from adafruit_seesaw.seesaw import Seesaw
        import RPi.GPIO as GPIO
        import atexit
        import datetime

        # GPIO setup
        rc1 = 24  # Light control pin
        rc2 = 23  # Pump control pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rc1, GPIO.OUT)
        GPIO.output(rc1, False)
        GPIO.setup(rc2, GPIO.OUT)
        GPIO.output(rc2, False)

        # Cleanup GPIO on exit
        def cleanup_gpio():
            GPIO.cleanup()

        atexit.register(cleanup_gpio)

        # I2C initialization and sensors setup
        i2c = board.I2C()
        veml7700 = adafruit_veml7700.VEML7700(i2c)
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
        bme680.sea_level_pressure = 1013.25
        ss = Seesaw(i2c, addr=0x36)

        def read_sensors():
            """Read data from real sensors."""
            timestamp = datetime.datetime.now()
            temperature = round(bme680.temperature, 2)
            gas = round(bme680.gas, 2)
            humidity = round(bme680.humidity, 2)
            pressure = round(bme680.pressure, 2)
            altitude = round(bme680.altitude, 2)
            luminosity = round(veml7700.light, 2)
            soil_moisture = round(ss.moisture_read(), 2)
            soil_temperature = round(ss.get_temp(), 2)
            return timestamp, temperature, gas, humidity, pressure, altitude, luminosity, soil_moisture, soil_temperature

        def control_led(luminosity):
            """Control the LED based on luminosity."""
            if luminosity >= 100:
                print("Lights are OFF")
                GPIO.output(rc1, True)
            else:
                print("Lights are ON")
                GPIO.output(rc1, False)

        def control_pump(soil_moisture):
            """Control the water pump based on soil moisture."""
            if soil_moisture <= 400:
                print("Pump is OFF")
                GPIO.output(rc2, True)
            else:
                print("Pump is ON")
                GPIO.output(rc2, False)

        def main_loop():
            """Read and store real sensor data."""
            while True:
                try:
                    # Step 1: Read real sensor data
                    data = read_sensors()

                    # Step 2: Store the data in the database
                    store_data(data)

                    # Step 3: Print data to console
                    print(f"Stored real sensor data: {data}")

                    # Delay for real sensor readings
                    time.sleep(1)
                except Exception as e:
                    print(f"Error in production loop: {e}")
                    break

    except ImportError as e:
        # Fallback to simulated mode
        print(f"Error importing Raspberry Pi libraries: {e}")
        print("Falling back to simulated sensor data (development mode).")
        from app.sensor_dev import read_sensors, control_led, control_pump

# Run the main loop in a background thread
if __name__ == "__main__":
    threading.Thread(target=main_loop, daemon=True).start()
    print("Sensor loop started in background thread.")
    while True:
        time.sleep(1)  # Keep the main thread alive
