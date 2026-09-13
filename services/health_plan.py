from agents.dietary_agent import dietary_planner
from agents.fitness_agent import fitness_trainer
from agents.team_lead_agent import team_lead

from services.health_calculations import (
    calculate_health_metrics
)


# ============================================================
# MEAL PLAN
# ============================================================

def get_meal_plan(
    age,
    weight,
    height,
    activity_level,
    dietary_preference,
    fitness_goal,
    metrics
):

    prompt = f"""
Create a personalized meal plan.

User Information:

Age: {age}
Weight: {weight} kg
Height: {height} cm

Activity Level:
{activity_level}

Dietary Preference:
{dietary_preference}

Fitness Goal:
{fitness_goal}

Calculated Health Metrics:

BMI: {metrics["BMI"]}

BMR:
{metrics["BMR"]} calories/day

TDEE:
{metrics["TDEE"]} calories/day

Daily Calorie Target:
{metrics["Daily Calories"]} calories

Daily Protein Target:
{metrics["Daily Protein"]} grams

Create a practical daily meal plan containing:

1. Breakfast
2. Morning snack
3. Lunch
4. Evening snack
5. Dinner
6. Hydration recommendations
7. Approximate calories
8. Approximate protein

Make sure the meal plan aligns with the user's
dietary preference and fitness goal.
"""

    return dietary_planner.run(prompt)


# ============================================================
# FITNESS PLAN
# ============================================================

def get_fitness_plan(
    age,
    weight,
    height,
    activity_level,
    fitness_goal
):

    prompt = f"""
Generate a personalized workout plan.

User Information:

Age: {age}
Weight: {weight} kg
Height: {height} cm

Activity Level:
{activity_level}

Fitness Goal:
{fitness_goal}

Create a structured workout plan including:

1. Warm-up
2. Main workout
3. Sets and repetitions where appropriate
4. Rest periods
5. Cool-down
6. Weekly schedule
7. Progress tracking
8. Safety recommendations

Make the plan appropriate for the user's
fitness goal and activity level.
"""

    return fitness_trainer.run(prompt)


# ============================================================
# FULL HEALTH PLAN
# ============================================================

def get_full_health_plan(
    name,
    age,
    weight,
    height,
    activity_level,
    dietary_preference,
    fitness_goal,
    progress_history
):

    # ========================================================
    # CALCULATE HEALTH METRICS
    # ========================================================

    metrics = calculate_health_metrics(
        age,
        weight,
        height,
        activity_level,
        fitness_goal
    )


    # ========================================================
    # GENERATE MEAL PLAN
    # ========================================================

    meal_plan = get_meal_plan(
        age,
        weight,
        height,
        activity_level,
        dietary_preference,
        fitness_goal,
        metrics
    )


    # ========================================================
    # GENERATE WORKOUT PLAN
    # ========================================================

    fitness_plan = get_fitness_plan(
        age,
        weight,
        height,
        activity_level,
        fitness_goal
    )


    # ========================================================
    # FINAL TEAM LEAD PROMPT
    # ========================================================

    final_prompt = f"""
Greet the customer by name:

{name}

========================================
USER INFORMATION
========================================

Age:
{age}

Weight:
{weight} kg

Height:
{height} cm

Activity Level:
{activity_level}

Dietary Preference:
{dietary_preference}

Fitness Goal:
{fitness_goal}


========================================
CALCULATED HEALTH METRICS
========================================

BMI:
{metrics["BMI"]}

BMI Category:
{metrics["BMI Category"]}

BMR:
{metrics["BMR"]} calories/day

TDEE:
{metrics["TDEE"]} calories/day

Daily Calorie Target:
{metrics["Daily Calories"]} calories

Daily Protein Target:
{metrics["Daily Protein"]} grams


========================================
MEAL PLAN
========================================

{meal_plan.content}


========================================
WORKOUT PLAN
========================================

{fitness_plan.content}


========================================
PREVIOUS PROGRESS
========================================

{progress_history}


========================================
TASK
========================================

Create a comprehensive personalized health
and fitness strategy.

Include:

1. Personal summary
2. BMI and health metric explanation
3. Recommended calorie target
4. Protein target
5. Daily meal plan
6. Weekly workout plan
7. Hydration recommendations
8. Lifestyle recommendations
9. Progress tracking recommendations
10. Suggestions for adjusting the plan
    based on previous progress

Use tables where appropriate.

Keep the recommendations practical and easy
to follow.

Clearly state that this is general wellness
guidance and not a substitute for professional
medical advice.
"""


    # ========================================================
    # RETURN FINAL RESULT
    # ========================================================

    return team_lead.run(
        final_prompt
    )