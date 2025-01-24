
from __future__ import annotations

import os
import sqlite3
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_ai import Agent, ModelRetry, RunContext

###############################################################################
# 1) Load .env (if using OPENAI_API_KEY via environment variables)
###############################################################################
load_dotenv()

###############################################################################
# 2) Define Dependencies
###############################################################################
@dataclass
class Deps:
    db_path: str  # e.g., "data/Neutrino.db"

###############################################################################
# 3) Valid Columns in SensorsData
###############################################################################
VALID_COLUMNS = {
    "temperature": "Temperature",
    "gas": "Gas",
    "humidity": "Humidity",
    "pressure": "Pressure",
    "altitude": "Altitude",
    "luminosity": "Luminosity",
    "soil_moisture": "soil_moisture",
    "soil_temperature": "soil_temperature",
}

###############################################################################
# 4) Create the PydenticAI Agent
###############################################################################
garden_agent = Agent(
    # Use whichever OpenAI model you have access to.
    # (Make sure you have GPT-3.5 or GPT-4 privileges.)
    "openai:gpt-3.5-turbo",

    system_prompt=(
        "You have access to a SQLite table named SensorsData, which has columns: "
        "TimeStamp, Temperature, Gas, Humidity, Pressure, Altitude, Luminosity, "
        "soil_moisture, soil_temperature. Use the tool `get_sensor_data` to retrieve "
        "the latest reading of one of these columns whenever a user asks about it. "
        "The user might say 'What is the latest temperature?' or 'Give me the humidity.' "
        "You must call `get_sensor_data(\"temperature\")` or `get_sensor_data(\"humidity\")`, etc. "
        "Return concise answers."
    ),
    retries=2,
)

###############################################################################
# 5) Define the Flexible "Tool" that Adapts to Different Columns
###############################################################################
@garden_agent.tool
async def get_sensor_data(ctx: RunContext[Deps], variable_name: str) -> str:
    """
    Retrieve the latest reading for one of the valid columns in SensorsData.

    variable_name should be one of:
    'temperature', 'gas', 'humidity', 'pressure', 'altitude',
    'luminosity', 'soil_moisture', or 'soil_temperature'.
    """
    db_path = ctx.deps.db_path

    # Normalize the variable name (lowercase, strip whitespace)
    var_lower = variable_name.lower().strip()

    # Validate that it's in our known columns dict
    if var_lower not in VALID_COLUMNS:
        valid_list = ", ".join(VALID_COLUMNS.keys())
        return f"Invalid sensor name '{variable_name}'. Valid options: {valid_list}."

    # Map "temperature" -> "Temperature", etc.
    column_name = VALID_COLUMNS[var_lower]

    # Construct query to get the most recent row for that column
    query = f"""
        SELECT {column_name}, TimeStamp
        FROM SensorsData
        ORDER BY TimeStamp DESC
        LIMIT 1
    """

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        conn.close()

        if row:
            value, ts = row
            return f"The latest {variable_name} reading is {value} at {ts}."
        else:
            return f"No {variable_name} data found in the database."

    except Exception as e:
        raise ModelRetry(f"Database error: {str(e)}")
