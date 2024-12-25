import os
import sqlite3
from app.db import store_data, fetch_latest_data
from app.sensor_dev import read_sensors

# Use absolute path for the database file
DB_NAME = os.path.abspath("../data/Neutrino.db")

def check_database_table():
    """Check if the SensorsData table exists in the database."""
    print("Checking if the SensorsData table exists...")

    # Ensure the `data/` directory exists
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='SensorsData'")
        table_exists = cursor.fetchone() is not None
        if table_exists:
            print("Table 'SensorsData' exists.")
        else:
            print("Table 'SensorsData' does not exist. Please create it before running the test.")
    except sqlite3.Error as e:
        print(f"Error checking table: {e}")
    finally:
        conn.close()

def test_database_write_and_read():
    """Test if data is correctly written to and read from the database."""
    print("Starting database test...")

    # Step 1: Generate random sensor data
    test_data = read_sensors()
    print(f"Generated test data: {test_data}")

    # Step 2: Write the generated data to the database
    store_data(test_data)
    print("Data written to the database.")

    # Step 3: Fetch the latest data from the database
    fetched_data = fetch_latest_data()
    print(f"Fetched data: {fetched_data}")

    # Step 4: Verify that the written and fetched data match
    if fetched_data is not None:
        # Reformat the test data for comparison (convert timestamp to string)
        test_data_str = (
            test_data[0].strftime('%Y-%m-%d %H:%M:%S'),  # Format timestamp
            *test_data[1:]
        )
        matches = fetched_data == test_data_str
        if matches:
            print("Test passed: Data written and read from the database match.")
        else:
            print(f"Test failed: Data mismatch.\nWritten: {test_data_str}\nFetched: {fetched_data}")
    else:
        print("Test failed: No data fetched from the database.")

if __name__ == "__main__":
    # Debugging: Print resolved database path
    print(f"Resolved database path: {DB_NAME}")

    # Check if the database table exists
    check_database_table()

    # Run the database write and read test
    test_database_write_and_read()
