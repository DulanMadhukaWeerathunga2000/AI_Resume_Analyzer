import sqlite3
import json

DATABASE = "resume_analyzer.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_database():

    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            matched_skills TEXT DEFAULT '[]',
            missing_skills TEXT DEFAULT '[]',
            suggestions TEXT DEFAULT '[]',
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

    connection.execute("""
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

    rows = connection.execute("""
        SELECT *
        FROM analyses
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return rows


def delete_analysis(analysis_id):

    connection = get_connection()

    connection.execute(
        "DELETE FROM analyses WHERE id = ?",
        (analysis_id,)
    )

    connection.commit()
    connection.close()