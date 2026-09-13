import os
import streamlit as st

from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools


# ============================================================
# API KEY
# ============================================================

GOOGLE_API_KEY = st.secrets.get(
    "GOOGLE_API_KEY",
    os.environ.get("GOOGLE_API_KEY")
)

if not GOOGLE_API_KEY:
    raise ValueError(
        "No Gemini API key found. Set GOOGLE_API_KEY "
        "in .streamlit/secrets.toml."
    )

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# ============================================================
# DIETARY PLANNER AGENT
# ============================================================

dietary_planner = Agent(

    model=Gemini(
        id="gemini-3.1-flash-lite"
    ),

    description=(
        "Creates personalized dietary plans "
        "based on user information and health goals."
    ),

    instructions=[

        "Generate a diet plan with breakfast, lunch, dinner, and snacks.",

        "Consider dietary preferences such as "
        "Keto, Vegetarian, Low Carb, or Balanced.",

        "Ensure proper hydration and electrolyte balance.",

        "Provide nutritional breakdown including "
        "macronutrients and important vitamins.",

        "Suggest practical meal preparation tips.",

        "Use the provided calorie and protein targets "
        "when creating the meal plan.",

        "If necessary, search the web using DuckDuckGo "
        "for additional information.",

        "Do not claim to diagnose or treat medical conditions.",

        "Clearly mention that the plan is general wellness "
        "guidance and not a substitute for professional medical advice."
    ],

    tools=[
        DuckDuckGoTools()
    ],

    markdown=True
)