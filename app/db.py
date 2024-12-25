import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "../data/Neutrino.db")
print(f"Resolved database path: {DB_NAME}")  # Debugging

def fetch_latest_data():
    """Fetch the most recent sensor data."""
    try:
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()
        curs.execute("SELECT * FROM SensorsData ORDER BY timestamp DESC LIMIT 1")
        data = curs.fetchone()
        conn.close()
        print("Fetched data:", data)  # Debugging
        return data
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return None

def store_data(data):
    """Store sensor data into the database."""
    conn = None  # Initialize to None
    try:
        print(f"Storing data: {data}")  # Debugging: Log the data being stored
        conn = sqlite3.connect(DB_NAME)  # Attempt to connect to the database
        curs = conn.cursor()

        # Ensure timestamp is a string
        data_with_timestamp_str = (
            data[0].strftime('%Y-%m-%d %H:%M:%S'),
            *data[1:]
        )

        # Insert data into the database
        curs.execute('''
            INSERT INTO SensorsData (timestamp, temperature, gas, humidity, pressure, altitude, luminosity, soil_moisture, soil_temperature)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', data_with_timestamp_str)

        conn.commit()
        print("Data committed successfully.")  # Debugging: Log success
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Debugging: Log the error
    except Exception as e:
        print(f"Unexpected error: {e}")  # Debugging: Catch all other exceptions
    finally:
        # Safely close the connection if it was successfully created
        if conn:
            conn.close()
