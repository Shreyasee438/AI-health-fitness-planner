def calculate_health_metrics(
    age,
    weight,
    height,
    activity_level,
    fitness_goal
):
    """
    Calculate BMI, BMR, TDEE, calorie target
    and daily protein target.
    """

    # ========================================================
    # BMI
    # ========================================================

    height_m = height / 100

    bmi = weight / (height_m ** 2)


    # ========================================================
    # BMR
    # ========================================================
    # Simplified Mifflin-St Jeor estimate.
    # The current UI does not ask for gender.
    # ========================================================

    bmr = (
        (10 * weight)
        + (6.25 * height)
        - (5 * age)
        + 5
    )


    # ========================================================
    # ACTIVITY MULTIPLIER
    # ========================================================

    activity_multipliers = {

        "Low": 1.2,

        "Moderate": 1.55,

        "High": 1.725
    }


    tdee = (
        bmr
        * activity_multipliers[activity_level]
    )


    # ========================================================
    # CALORIE TARGET
    # ========================================================

    if fitness_goal == "Weight Loss":

        calorie_target = tdee - 500

    elif fitness_goal == "Muscle Gain":

        calorie_target = tdee + 300

    else:

        calorie_target = tdee


    # ========================================================
    # PROTEIN TARGET
    # ========================================================

    if fitness_goal == "Muscle Gain":

        protein_target = weight * 1.6

    elif fitness_goal == "Weight Loss":

        protein_target = weight * 1.5

    else:

        protein_target = weight * 1.2


    # ========================================================
    # BMI CATEGORY
    # ========================================================

    if bmi < 18.5:

        bmi_category = "Underweight"

    elif bmi < 25:

        bmi_category = "Normal Weight"

    elif bmi < 30:

        bmi_category = "Overweight"

    else:

        bmi_category = "Obesity"


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "BMI": round(bmi, 2),

        "BMI Category": bmi_category,

        "BMR": round(bmr),

        "TDEE": round(tdee),

        "Daily Calories": round(calorie_target),

        "Daily Protein": round(protein_target)
    }