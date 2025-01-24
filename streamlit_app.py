# streamlit_app.py
import asyncio
import os

import streamlit as st

from app.agents.ai_agent import garden_agent, Deps  # Your existing agent code

# Ensure you have a matching or updated version of Streamlit that supports chat_input.
# pip install --upgrade streamlit

def main():
    st.set_page_config(page_title="SmartGarden AI Chat", layout="centered")

    st.title("SmartGarden AI Chat \U0001F331")

    # Maintain the conversation (history) in session_state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 1. Display existing chat messages (User / Agent)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 2. Chat input box (Pressing Enter will trigger the below block)
    user_input = st.chat_input("Ask about your garden sensors (e.g., temperature, humidity, etc.)")
    if user_input:
        # The user pressed Enter on the chat input
        # 2a. Add user message to the conversation
        st.session_state.messages.append({"role": "user", "content": user_input})

        # 2b. Display the user's message
        with st.chat_message("user"):
            st.write(user_input)

        # 2c. Call the agent asynchronously
        answer = asyncio.run(call_agent(user_input))

        # 2d. Display agent's response
        with st.chat_message("assistant"):
            st.write(answer)

        # 2e. Save to conversation
        st.session_state.messages.append({"role": "assistant", "content": answer})


async def call_agent(user_query: str) -> str:
    """Asynchronously call the garden_agent with the user query."""
    # Path to your DB
    db_path = os.path.join("data", "Neutrino.db")
    deps = Deps(db_path=db_path)

    # pydentic-ai is async, so we use await
    result = await garden_agent.run(user_query, deps=deps)
    return result.data

if __name__ == "__main__":
    main()
