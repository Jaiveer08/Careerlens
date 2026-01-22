import sqlite3
from datetime import datetime

DB_NAME = "career_lens.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        skills_found TEXT,
        missing_skills TEXT,
        score INTEGER,
        created_at TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_analysis(role, skills_found, missing_skills, score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO resume_analysis (role, skills_found, missing_skills, score, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        role,
        ", ".join(skills_found),
        ", ".join(missing_skills),
        score,
        datetime.now()
    ))

    conn.commit()
    conn.close()