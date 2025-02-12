import sqlite3

def fetch_latest_sensor_data(db_path: str, column_name: str):
    """Fetch the latest reading for a given sensor."""
    query = f"SELECT {column_name}, TimeStamp FROM SensorsData ORDER BY TimeStamp DESC LIMIT 1"
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()
