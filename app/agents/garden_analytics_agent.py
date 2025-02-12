import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pandasai import SmartDataframe
from pandasai_local import LocalLLM  # Importing LocalLLM for local model integration
from dataclasses import dataclass

# Load environment variables
load_dotenv()

@dataclass
class Deps:
    db_path: str

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

class GardenAnalyticsAgent:
    def __init__(self, model="openai:gpt-4"):
        # Load model configuration
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

        if isinstance(model, str) and model.startswith("ollama"):
            self.model = OpenAIModel(model_name=model.replace("ollama:", ""), base_url=base_url)
            self.llm = LocalLLM(api_base=base_url, model=model.replace("ollama:", ""))  # Using LocalLLM for local models
        else:
            self.model = model
            self.llm = OpenAIModel(model_name=model)

        self.agent = Agent(
            self.model,
            system_prompt="You analyze Smart Garden data, fetch real-time sensor readings, and generate insights."
        )

        # Register tools
        self.agent.tool(self.get_sensor_data)
        self.agent.tool(self.get_highest_temperature_today)
        self.agent.tool(self.query_pandasai)

    async def get_sensor_data(self, ctx: RunContext[Deps], variable_name: str) -> str:
        """Fetch the latest sensor reading from the database."""
        db_path = ctx.deps.db_path
        column_name = VALID_COLUMNS.get(variable_name.lower())

        if not column_name:
            return "Invalid sensor name."

        query = f"SELECT {column_name}, TimeStamp FROM SensorsData ORDER BY TimeStamp DESC LIMIT 1"

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            conn.close()

            return f"The latest {variable_name} reading is {row[0]} at {row[1]}" if row else "No data found."
        except Exception as e:
            return f"Database error: {str(e)}"

    async def get_highest_temperature_today(self, ctx: RunContext[Deps]) -> str:
        """Return the highest recorded temperature today."""
        db_path = ctx.deps.db_path
        query = "SELECT MAX(Temperature) FROM SensorsData WHERE DATE(TimeStamp) = DATE('now')"

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            max_temp = cursor.fetchone()[0]
            conn.close()
            return f"The highest temperature today is {max_temp}°C."
        except Exception as e:
            return f"Database error: {str(e)}"

    async def query_pandasai(self, ctx: RunContext[Deps], query: str) -> str:
        """Use PandasAI to analyze Smart Garden data with natural language queries."""
        db_path = ctx.deps.db_path

        try:
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query("SELECT * FROM SensorsData", conn)
            conn.close()

            # Create a SmartDataframe with the configured LLM
            sdf = SmartDataframe(df, config={"llm": self.llm})

            # Process natural language query
            response = sdf.chat(query)

            return str(response)  # Convert PandasAI response to a string
        except Exception as e:
            return f"Error processing PandasAI query: {str(e)}"
