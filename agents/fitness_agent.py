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
# FITNESS TRAINER AGENT
# ============================================================

fitness_trainer = Agent(

    model=Gemini(
        id="gemini-3.1-flash-lite"
    ),

    description=(
        "Generates customized workout routines "
        "based on fitness goals."
    ),

    instructions=[

        "Create workout plans including warm-ups, "
        "main exercises, and cool-downs.",

        "Adjust workouts based on the user's activity level.",

        "Consider goals such as weight loss, muscle gain, "
        "endurance, and flexibility.",

        "Provide beginner-friendly instructions when appropriate.",

        "Provide safety tips and injury-prevention advice.",

        "Suggest progress-tracking methods.",

        "Do not claim to diagnose or treat medical conditions.",

        "If necessary, search the web using DuckDuckGo "
        "for additional information.",

        "Clearly state that users should consult a qualified "
        "professional for medical or injury-related concerns."
    ],

    tools=[
        DuckDuckGoTools()
    ],

    markdown=True
)