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
            missing_skills TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(filename, score, matched, missing):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyses
        (filename, score, matched_skills, missing_skills)
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        score,
        ", ".join(matched),
        ", ".join(missing)
    ))

    conn.commit()
    conn.close()