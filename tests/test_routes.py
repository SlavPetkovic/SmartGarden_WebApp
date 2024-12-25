from app.db import store_data, fetch_latest_data
from app.sensor_dev import read_sensors

data = read_sensors()
store_data(data)
print(fetch_latest_data())
