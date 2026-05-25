import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "stageready.db")


def _get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_db():
    conn = _get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS module_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            module_number INTEGER NOT NULL,
            notes TEXT,
            quiz_score INTEGER,
            quiz_passed BOOLEAN DEFAULT 0,
            submission_path TEXT,
            completed_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, module_number)
        )
    """)

    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = _get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = _get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user


def create_user(first_name, last_name, email, password_hash):
    conn = _get_connection()
    conn.execute(
        "INSERT INTO users (first_name, last_name, email, password_hash) VALUES (?, ?, ?, ?)",
        (first_name, last_name, email, password_hash)
    )
    conn.commit()
    conn.close()

def get_module_progress(user_id, module_number):
    conn = _get_connection()
    row = conn.execute(
        "SELECT * FROM module_progress WHERE user_id = ? AND module_number = ?",
        (user_id, module_number)
    ).fetchone()
    conn.close()
    return row


def get_all_progress(user_id):
    conn = _get_connection()
    rows = conn.execute(
        "SELECT * FROM module_progress WHERE user_id = ? ORDER BY module_number",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def save_notes(user_id, module_number, notes):
    conn = _get_connection()
    conn.execute("""
        INSERT INTO module_progress (user_id, module_number, notes)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, module_number)
        DO UPDATE SET notes = excluded.notes
    """, (user_id, module_number, notes))
    conn.commit()
    conn.close()


def set_quiz_result(user_id, module_number, score, passed):
    conn = _get_connection()
    conn.execute("""
        INSERT INTO module_progress (user_id, module_number, quiz_score, quiz_passed)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, module_number)
        DO UPDATE SET quiz_score = excluded.quiz_score, quiz_passed = excluded.quiz_passed
    """, (user_id, module_number, score, int(passed)))
    conn.commit()
    conn.close()


def save_submission(user_id, module_number, file_path):
    conn = _get_connection()
    conn.execute("""
        INSERT INTO module_progress (user_id, module_number, submission_path, completed_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, module_number)
        DO UPDATE SET submission_path = excluded.submission_path,
                      completed_at = excluded.completed_at
    """, (user_id, module_number, file_path))
    conn.commit()
    conn.close()
