import os
import openai
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pandasai import SmartDataframe
from pandasai_openai import OpenAI
from sqlalchemy import create_engine

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Connect to SQLite database
DB_PATH = "../data/Neutrino.db"
engine = create_engine(f"sqlite:///{DB_PATH}")


def fetch_data(query: str):
    """Execute a SQL query and return the result as a Pandas DataFrame."""
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


# Configure PandasAI with OpenAI
llm = OpenAI(api_token=openai.api_key)


def query_with_pandasai(df, query):
    """Use PandasAI to interpret user queries and return a response."""
    sdf = SmartDataframe(df, config={"llm": llm})
    return sdf.chat(query)


# Streamlit UI
st.title("Neutrino Data Agent")

user_input = st.text_input("Ask a question about sensor data:")

if user_input:
    query = "SELECT * FROM SensorsData ORDER BY TimeStamp DESC LIMIT 100"
    df = fetch_data(query)

    if not df.empty:
        response = query_with_pandasai(df, user_input)
        st.write(response)

        if "chart" in user_input.lower():
            st.write("Generating chart...")
            plt.figure(figsize=(10, 5))
            plt.plot(df['TimeStamp'], df['Temperature'], label='Temperature')
            plt.plot(df['TimeStamp'], df['Humidity'], label='Humidity')
            plt.plot(df['TimeStamp'], df['Pressure'], label='Pressure')
            plt.xlabel('Time')
            plt.ylabel('Sensor Readings')
            plt.legend()
            plt.xticks(rotation=45)
            st.pyplot(plt)
    else:
        st.write("No data available.")
