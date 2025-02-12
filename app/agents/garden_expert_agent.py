import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables
load_dotenv()

class GardenExpertAgent:
    def __init__(self, model=None):
        # Load model from .env if not provided
        model_name = model or os.getenv("AI_MODEL", "openai:gpt-4")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

        if isinstance(model_name, str) and model_name.startswith("ollama"):
            self.model = OpenAIModel(model_name=model_name.replace("ollama:", ""), base_url=base_url)
        else:
            self.model = model_name

        self.agent = Agent(
            self.model,
            system_prompt="You are an expert in smart gardening. "
                          "You analyze data, give gardening advice, and answer user questions."
        )

        # ✅ Register tools
        self.agent.tool(self.give_gardening_tips)

    async def give_gardening_tips(self, ctx: RunContext) -> str:
        """
        Provide general gardening tips.
        """
        tips = [
            "Water plants in the morning to avoid water loss.",
            "Use mulch to retain soil moisture.",
            "Adjust lighting based on plant needs.",
            "Prune plants to encourage growth.",
            "Check soil pH for optimal nutrient absorption.",
        ]
        return "🌿 Smart Gardening Tips:\n- " + "\n- ".join(tips)
