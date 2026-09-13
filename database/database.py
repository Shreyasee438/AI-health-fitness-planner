import sqlite3


DATABASE_NAME = "health_fitness.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        date TEXT NOT NULL,

        weight REAL NOT NULL,

        workout_days INTEGER NOT NULL,

        steps INTEGER NOT NULL

    )
    """)


    conn.commit()

    conn.close()


# ============================================================
# SAVE PROGRESS
# ============================================================

def save_progress(
    name,
    date,
    weight,
    workout_days,
    steps
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO progress
        (
            name,
            date,
            weight,
            workout_days,
            steps
        )
        VALUES (?, ?, ?, ?, ?)
        """,

        (
            name,
            date,
            weight,
            workout_days,
            steps
        )
    )


    conn.commit()

    conn.close()


# ============================================================
# GET PROGRESS HISTORY
# ============================================================

def get_progress_history(name):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            date,
            weight,
            workout_days,
            steps
        FROM progress
        WHERE name = ?
        ORDER BY date
        """,

        (name,)
    )


    rows = cursor.fetchall()

    conn.close()


    return rows