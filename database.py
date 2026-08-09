import sqlite3
import json
from pathlib import Path


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "resume_analyzer.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            job_description TEXT,

            -- Old version compatibility
            score INTEGER NOT NULL DEFAULT 0,

            -- New scores
            match_score INTEGER NOT NULL DEFAULT 0,
            ats_score INTEGER NOT NULL DEFAULT 0,
            technical_score INTEGER NOT NULL DEFAULT 0,
            soft_score INTEGER NOT NULL DEFAULT 0,

            -- Analysis data
            matched_keywords TEXT DEFAULT '[]',
            missing_keywords TEXT DEFAULT '[]',

            strengths TEXT DEFAULT '[]',
            suggestions TEXT DEFAULT '[]',
            recommended_skills TEXT DEFAULT '[]',

            sections TEXT DEFAULT '{}',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    # =====================================================
    # CHECK EXISTING COLUMNS
    # =====================================================

    cursor.execute("PRAGMA table_info(analyses)")

    existing_columns = {
        row["name"]
        for row in cursor.fetchall()
    }

    # =====================================================
    # REQUIRED COLUMNS
    # =====================================================

    required_columns = {

        "filename":
            "TEXT",

        "job_description":
            "TEXT",

        # IMPORTANT:
        # This fixes:
        # sqlite3.IntegrityError:
        # NOT NULL constraint failed: analyses.score
        "score":
            "INTEGER NOT NULL DEFAULT 0",

        "match_score":
            "INTEGER NOT NULL DEFAULT 0",

        "ats_score":
            "INTEGER NOT NULL DEFAULT 0",

        "technical_score":
            "INTEGER NOT NULL DEFAULT 0",

        "soft_score":
            "INTEGER NOT NULL DEFAULT 0",

        "matched_keywords":
            "TEXT DEFAULT '[]'",

        "missing_keywords":
            "TEXT DEFAULT '[]'",

        "strengths":
            "TEXT DEFAULT '[]'",

        "suggestions":
            "TEXT DEFAULT '[]'",

        "recommended_skills":
            "TEXT DEFAULT '[]'",

        "sections":
            "TEXT DEFAULT '{}'",

        "created_at":
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    }

    # =====================================================
    # ADD MISSING COLUMNS
    # =====================================================

    for column, definition in required_columns.items():

        if column not in existing_columns:

            try:

                cursor.execute(
                    f"""
                    ALTER TABLE analyses
                    ADD COLUMN {column} {definition}
                    """
                )

                print(
                    f"[DATABASE] Added missing column: {column}"
                )

            except sqlite3.OperationalError as error:

                print(
                    f"[DATABASE] Could not add column "
                    f"{column}: {error}"
                )

    connection.commit()

    # =====================================================
    # FIX OLD NULL VALUES
    # =====================================================

    update_queries = [

        """
        UPDATE analyses
        SET score = 0
        WHERE score IS NULL
        """,

        """
        UPDATE analyses
        SET match_score = score
        WHERE match_score IS NULL
        """,

        """
        UPDATE analyses
        SET ats_score = 0
        WHERE ats_score IS NULL
        """,

        """
        UPDATE analyses
        SET technical_score = 0
        WHERE technical_score IS NULL
        """,

        """
        UPDATE analyses
        SET soft_score = 0
        WHERE soft_score IS NULL
        """
    ]

    for query in update_queries:

        try:
            cursor.execute(query)

        except sqlite3.OperationalError:
            pass

    connection.commit()
    connection.close()

    print("[DATABASE] Database initialized successfully.")


# =========================================================
# SAVE ANALYSIS
# =========================================================

def save_analysis(filename, job_description, result):

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # Get values from analysis result
    # -----------------------------------------------------

    match_score = int(
        result.get("match_score", 0)
    )

    ats_score = int(
        result.get("ats_score", 0)
    )

    technical_score = int(
        result.get("technical_score", 0)
    )

    soft_score = int(
        result.get("soft_score", 0)
    )

    matched_keywords = result.get(
        "matched_keywords",
        []
    )

    missing_keywords = result.get(
        "missing_keywords",
        []
    )

    strengths = result.get(
        "strengths",
        []
    )

    suggestions = result.get(
        "suggestions",
        []
    )

    recommended_skills = result.get(
        "recommended_skills",
        []
    )

    sections = result.get(
        "sections",
        {}
    )

    # -----------------------------------------------------
    # IMPORTANT
    #
    # Old database has:
    #
    # score INTEGER NOT NULL
    #
    # So we save match_score into score as well.
    # -----------------------------------------------------

    old_score = match_score

    cursor.execute("""
        INSERT INTO analyses (

            filename,

            job_description,

            score,

            match_score,

            ats_score,

            technical_score,

            soft_score,

            matched_keywords,

            missing_keywords,

            strengths,

            suggestions,

            recommended_skills,

            sections

        )

        VALUES (

            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?

        )
    """, (

        filename,

        job_description,

        old_score,

        match_score,

        ats_score,

        technical_score,

        soft_score,

        json.dumps(
            matched_keywords,
            ensure_ascii=False
        ),

        json.dumps(
            missing_keywords,
            ensure_ascii=False
        ),

        json.dumps(
            strengths,
            ensure_ascii=False
        ),

        json.dumps(
            suggestions,
            ensure_ascii=False
        ),

        json.dumps(
            recommended_skills,
            ensure_ascii=False
        ),

        json.dumps(
            sections,
            ensure_ascii=False
        )
    ))

    analysis_id = cursor.lastrowid

    connection.commit()
    connection.close()

    print(
        f"[DATABASE] Analysis saved successfully. "
        f"ID = {analysis_id}"
    )

    return analysis_id


# =========================================================
# JSON DECODER
# =========================================================

def decode_json(value, default):

    if value is None:
        return default

    if value == "":
        return default

    try:

        return json.loads(value)

    except (
        TypeError,
        json.JSONDecodeError
    ):

        return default


# =========================================================
# CONVERT DATABASE ROW TO DICTIONARY
# =========================================================

def row_to_dict(row):

    if not row:
        return None

    data = dict(row)

    # -----------------------------------------------------
    # Decode JSON fields
    # -----------------------------------------------------

    data["matched_keywords"] = decode_json(
        data.get("matched_keywords"),
        []
    )

    data["missing_keywords"] = decode_json(
        data.get("missing_keywords"),
        []
    )

    data["strengths"] = decode_json(
        data.get("strengths"),
        []
    )

    data["suggestions"] = decode_json(
        data.get("suggestions"),
        []
    )

    data["recommended_skills"] = decode_json(
        data.get("recommended_skills"),
        []
    )

    data["sections"] = decode_json(
        data.get("sections"),
        {}
    )

    # -----------------------------------------------------
    # Backward compatibility
    #
    # If an old record has score but no match_score,
    # use score.
    # -----------------------------------------------------

    match_score = data.get(
        "match_score"
    )

    if match_score is None:

        match_score = data.get(
            "score",
            0
        )

    # -----------------------------------------------------
    # Create result object
    # -----------------------------------------------------

    data["result"] = {

        "match_score":
            int(match_score or 0),

        "ats_score":
            int(
                data.get(
                    "ats_score",
                    0
                ) or 0
            ),

        "technical_score":
            int(
                data.get(
                    "technical_score",
                    0
                ) or 0
            ),

        "soft_score":
            int(
                data.get(
                    "soft_score",
                    0
                ) or 0
            ),

        "matched_keywords":
            data["matched_keywords"],

        "missing_keywords":
            data["missing_keywords"],

        "strengths":
            data["strengths"],

        "suggestions":
            data["suggestions"],

        "recommended_skills":
            data["recommended_skills"],

        "sections":
            data["sections"]
    }

    return data


# =========================================================
# GET ALL ANALYSES
# =========================================================

def get_all_analyses():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    analyses = []

    for row in rows:

        analyses.append(
            row_to_dict(row)
        )

    return analyses


# =========================================================
# GET SINGLE ANALYSIS
# =========================================================

def get_analysis(analysis_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        WHERE id = ?
    """, (
        analysis_id,
    ))

    row = cursor.fetchone()

    connection.close()

    return row_to_dict(row)


# =========================================================
# TEST DATABASE
# =========================================================

if __name__ == "__main__":

    print()
    print("===================================")
    print(" AI RESUME ANALYZER DATABASE")
    print("===================================")
    print()

    init_db()

    print()
    print(f"Database location:")
    print(DB_PATH)

    print()
    print("Database is ready.")