import streamlit as st
import pandas as pd
from datetime import datetime

from services.health_calculations import calculate_health_metrics
from services.health_plan import get_full_health_plan

from database.database import (
    initialize_database,
    save_progress,
    get_progress_history
)


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FitHealth",
    page_icon="🏋️‍♂️",
    layout="wide"
)


# ============================================================
# 2. SESSION STATE
# ============================================================

# Store the generated health plan so it survives Streamlit reruns.
if "health_plan" not in st.session_state:
    st.session_state.health_plan = None


# ============================================================
# 3. DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# 4. CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #FF6347;
}

.subtitle {
    text-align: center;
    font-size: 24px;
    color: #4CAF50;
}

.goal-card {
    padding: 20px;
    margin: 10px;
    background-color: #FFFFFF;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 5. APPLICATION HEADER
# ============================================================

st.markdown(
    '<h1 class="title">'
    '🏋️‍♂️ FitHealth'
    '</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">'
    'Personalized fitness and nutrition plans powered by AI!'
    '</p>',
    unsafe_allow_html=True
)


# ============================================================
# 6. SIDEBAR INPUTS
# ============================================================

st.sidebar.header("⚙️ Health & Fitness Inputs")

st.sidebar.subheader(
    "Personalize Your Fitness Plan"
)


age = st.sidebar.number_input(
    "Age (in years)",
    min_value=10,
    max_value=100,
    value=25
)


weight = st.sidebar.number_input(
    "Weight (in kg)",
    min_value=30.0,
    max_value=200.0,
    value=70.0
)


height = st.sidebar.number_input(
    "Height (in cm)",
    min_value=100.0,
    max_value=250.0,
    value=170.0
)


activity_level = st.sidebar.selectbox(
    "Activity Level",
    [
        "Low",
        "Moderate",
        "High"
    ]
)


dietary_preference = st.sidebar.selectbox(
    "Dietary Preference",
    [
        "Keto",
        "Vegetarian",
        "Low Carb",
        "Balanced"
    ]
)


fitness_goal = st.sidebar.selectbox(
    "Fitness Goal",
    [
        "Weight Loss",
        "Muscle Gain",
        "Endurance",
        "Flexibility"
    ]
)


# ============================================================
# 7. USER PROFILE
# ============================================================

st.markdown("---")

st.markdown(
    "### 🏃‍♂️ Personal Fitness Profile"
)

name = st.text_input(
    "What's your name?",
    "John Doe"
)


# ============================================================
# 8. HEALTH METRICS
# ============================================================

metrics = calculate_health_metrics(
    age,
    weight,
    height,
    activity_level,
    fitness_goal
)


st.markdown("### 📊 Your Health Metrics")


col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        "BMI",
        metrics["BMI"]
    )


with col2:
    st.metric(
        "BMR",
        f'{metrics["BMR"]} kcal'
    )


with col3:
    st.metric(
        "TDEE",
        f'{metrics["TDEE"]} kcal'
    )


with col4:
    st.metric(
        "Daily Calories",
        f'{metrics["Daily Calories"]} kcal'
    )


with col5:
    st.metric(
        "Protein",
        f'{metrics["Daily Protein"]} g'
    )


st.caption(
    f'BMI Category: {metrics["BMI Category"]}'
)


# ============================================================
# 9. GENERATE HEALTH PLAN
# ============================================================

st.markdown("---")


if st.sidebar.button(
    "Generate Health Plan",
    type="primary"
):

    if not name.strip():

        st.warning("Please enter your name.")

    else:

        try:

            # ------------------------------------------------
            # Retrieve previous progress
            # ------------------------------------------------

            rows = get_progress_history(
                name.strip()
            )


            if rows:

                progress_history = "\n".join(
                    [
                        (
                            f"Date: {row[0]}, "
                            f"Weight: {row[1]} kg, "
                            f"Workout Days: {row[2]}, "
                            f"Steps: {row[3]}"
                        )
                        for row in rows
                    ]
                )

            else:

                progress_history = (
                    "No previous progress recorded."
                )


            # ------------------------------------------------
            # Generate AI plan
            # ------------------------------------------------

            with st.spinner(
                "💥 Generating your personalized "
                "health & fitness plan..."
            ):

                full_health_plan = get_full_health_plan(
                    name,
                    age,
                    weight,
                    height,
                    activity_level,
                    dietary_preference,
                    fitness_goal,
                    progress_history
                )


                # Store the generated plan in session state.
                # This keeps the plan available after reruns.
                st.session_state.health_plan = (
                    full_health_plan.content
                )


        except Exception as e:

            st.error(
                f"Something went wrong generating your plan: {e}"
            )


# ============================================================
# 10. DISPLAY GENERATED HEALTH PLAN
# ============================================================

if st.session_state.health_plan:

    st.subheader(
        "🎯 Your Personalized Health & Fitness Plan"
    )

    st.markdown(
        st.session_state.health_plan
    )

    st.info(
        "This plan provides general wellness guidance "
        "and should not replace advice from a qualified "
        "healthcare or fitness professional."
    )


# ============================================================
# 11. MOTIVATIONAL CARD
# ============================================================

st.markdown(
    """
<div class="goal-card">
    <h4>🏆 Stay Focused, Stay Fit!</h4>
    <p>
    Consistency is key. Track your progress,
    follow your plan, and make gradual adjustments
    over time.
    </p>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# 12. PROGRESS TRACKING
# ============================================================

st.markdown("---")

st.header("📈 Track Your Progress")

@st.fragment
def progress_tracking():

    # --------------------------------------------------------
    # Progress input form
    # --------------------------------------------------------

    with st.form("progress_form"):

        progress_date = st.date_input(
            "Progress Date",
            datetime.today()
        )

        current_weight = st.number_input(
            "Current Weight (kg)",
            min_value=30.0,
            max_value=200.0,
            value=float(weight)
        )

        workout_days = st.number_input(
            "Workout Days This Week",
            min_value=0,
            max_value=7,
            value=3
        )

        steps = st.number_input(
            "Average Daily Steps",
            min_value=0,
            max_value=50000,
            value=5000
        )

        save_button = st.form_submit_button(
            "💾 Save Progress"
        )


    # --------------------------------------------------------
    # Save Progress
    # --------------------------------------------------------

    if save_button:

        if not name.strip():

            st.warning(
                "Please enter your name before saving progress."
            )

        else:

            try:

                save_progress(
                    name=name.strip(),
                    date=str(progress_date),
                    weight=current_weight,
                    workout_days=workout_days,
                    steps=steps
                )

                st.success(
                    "✅ Progress saved successfully!"
                )

            except Exception as e:

                st.error(
                    f"Could not save progress: {e}"
                )


    # --------------------------------------------------------
    # Load Progress History
    # --------------------------------------------------------

    if name.strip():

        rows = get_progress_history(
            name.strip()
        )

        if rows:

            df = pd.DataFrame(
                rows,
                columns=[
                    "Date",
                    "Weight",
                    "Workout Days",
                    "Steps"
                ]
            )


            # ------------------------------------------------
            # Progress table
            # ------------------------------------------------

            st.subheader(
                "📋 Progress History"
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            # ------------------------------------------------
            # Prepare chart data
            # ------------------------------------------------

            chart_df = df.copy()

            chart_df["Date"] = pd.to_datetime(
                chart_df["Date"]
            )

            chart_df = chart_df.set_index(
                "Date"
            )


            # ------------------------------------------------
            # Weight chart
            # ------------------------------------------------

            st.subheader(
                "⚖️ Weight Progress"
            )

            st.line_chart(
                chart_df["Weight"]
            )


            # ------------------------------------------------
            # Workout chart
            # ------------------------------------------------

            st.subheader(
                "🏋️ Workout Consistency"
            )

            st.bar_chart(
                chart_df["Workout Days"]
            )


            # ------------------------------------------------
            # Steps chart
            # ------------------------------------------------

            st.subheader(
                "🚶 Daily Steps"
            )

            st.line_chart(
                chart_df["Steps"]
            )

        else:

            st.info(
                "No progress recorded yet. "
                "Save your first progress entry above."
            )


# Run progress tracking fragment
progress_tracking()


# ============================================================
# 13. FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🏋️ AI Health & Fitness Planner | "
    "Powered by Gemini + Agno + Streamlit"
)
