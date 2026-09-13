import os
import streamlit as st

from agno.agent import Agent
from agno.models.google import Gemini


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
# TEAM LEAD AGENT
# ============================================================

team_lead = Agent(

    model=Gemini(
        id="gemini-3.1-flash-lite"
    ),

    description=(
        "Combines dietary and fitness recommendations "
        "into a holistic health strategy."
    ),

    instructions=[

        "Merge the personalized diet and fitness plans.",

        "Ensure the diet and exercise recommendations "
        "are aligned with the user's fitness goal.",

        "Use tables where appropriate.",

        "Explain the calculated health metrics clearly.",

        "Suggest lifestyle habits for consistency.",

        "Suggest ways to monitor progress.",

        "Use previous progress information when provided.",

        "Recommend adjustments when progress indicates "
        "that the current strategy may need modification.",

        "Do not provide medical diagnosis or treatment."
    ],

    markdown=True
)