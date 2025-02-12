import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from app.agents.garden_analytics_agent import GardenAnalyticsAgent
from app.agents.garden_expert_agent import GardenExpertAgent
from dataclasses import dataclass

# Load environment variables
load_dotenv()

@dataclass
class Deps:
    db_path: str

class CoordinatorAgent:
    def __init__(self):
        # Load model from .env
        model_name = os.getenv("AI_MODEL", "openai:gpt-4")  # Default to GPT-4
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")  # Default Ollama API

        if isinstance(model_name, str) and model_name.startswith("ollama"):
            # If using Ollama, configure it as an OpenAI-compatible model
            self.model = OpenAIModel(model_name=model_name.replace("ollama:", ""), base_url=base_url)
        else:
            self.model = model_name  # Use OpenAI API directly

        self.agent = Agent(
            self.model,
            system_prompt=(
                "You are a coordinator for a Smart Garden system. "
                "Route user queries to the correct agent based on intent:\n"
                "- For real-time sensor values & analytics, call `query_analytics_agent`.\n"
                "- For gardening knowledge, call `query_expert_agent`."
            ),
        )

        # Pass only the model name (not the processed OpenAIModel)
        self.garden_analytics_agent = GardenAnalyticsAgent(model=model_name)
        self.garden_expert_agent = GardenExpertAgent(model=model_name)

        # Register tools
        self.agent.tool(self.query_analytics_agent)
        self.agent.tool(self.query_expert_agent)

    async def query_analytics_agent(self, ctx: RunContext[Deps], query: str) -> str:
        return await self.garden_analytics_agent.agent.run(query, deps=ctx.deps)

    async def query_expert_agent(self, ctx: RunContext[Deps], query: str) -> str:
        return await self.garden_expert_agent.agent.run(query, deps=ctx.deps)
