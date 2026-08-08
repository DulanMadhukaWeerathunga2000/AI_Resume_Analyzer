import sqlite3
import json


DATABASE = "resume_analyzer.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT NOT NULL,

            score INTEGER NOT NULL,

            matched_skills TEXT,

            missing_skills TEXT,

            suggestions TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


def save_analysis(
    filename,
    score,
    matched_skills,
    missing_skills,
    suggestions
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analyses
        (
            filename,
            score,
            matched_skills,
            missing_skills,
            suggestions
        )

        VALUES (?, ?, ?, ?, ?)
    """, (

        filename,

        score,

        json.dumps(matched_skills),

        json.dumps(missing_skills),

        json.dumps(suggestions)

    ))

    connection.commit()

    connection.close()


def get_all_analyses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            filename,
            score,
            matched_skills,
            missing_skills,
            suggestions,
            created_at

        FROM analyses

        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_analysis(analysis_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            filename,
            score,
            matched_skills,
            missing_skills,
            suggestions,
            created_at

        FROM analyses

        WHERE id = ?
    """, (analysis_id,))

    row = cursor.fetchone()

    connection.close()

    return row


def delete_analysis(analysis_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM analyses WHERE id = ?",
        (analysis_id,)
    )

    connection.commit()

    connection.close()