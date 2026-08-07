import sqlite3

DATABASE = "resume_analyzer.db"


def create_database():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()


def save_analysis(
    filename,
    score,
    matched,
    missing,
    suggestions
):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

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
        ", ".join(matched),
        ", ".join(missing),
        " | ".join(suggestions)
    ))

    conn.commit()
    conn.close()


def get_all_analyses():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

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
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data