import asyncio
import os
import base64
import streamlit as st
from dotenv import load_dotenv
from app.agents.coordinator_agent import CoordinatorAgent, Deps

# Load environment variables
load_dotenv()

# Initialize Coordinator Agent
coordinator_agent = CoordinatorAgent()

# Streamlit App
def main():
    st.set_page_config(page_title="SmartGarden AI Chat", layout="centered")
    st.title("🌱 SmartGarden AI Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask your garden AI something (e.g., temperature, analytics, tips, etc.)")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("Thinking..."):
            response = asyncio.run(handle_user_query(user_input))

        # FIX: Extract .data from response
        if isinstance(response.data, str) and response.data.startswith("data:image/png;base64,"):
            st.image(base64.b64decode(response.data.split(",")[1]))
        else:
            st.session_state.messages.append({"role": "assistant", "content": response.data})
            with st.chat_message("assistant"):
                st.write(response.data)

async def handle_user_query(query: str) -> str:
    """
    Handle user queries by passing them to the Coordinator Agent.
    """
    db_path = os.path.join("data", "Neutrino.db")

    # FIX: Extract .data from the RunResult object
    result = await coordinator_agent.agent.run(query, deps=Deps(db_path=db_path))
    return result  # Returns a RunResult object, but we will extract `.data` when needed

if __name__ == "__main__":
    main()
