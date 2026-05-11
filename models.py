import os
import sqlite3


BASE_DIR = os.path.dirname(__file__)
DATABASE_DIR = os.path.join(BASE_DIR, 'Database')
DATABASE = os.path.join(DATABASE_DIR, 'users.db')


def get_db_connection():
    os.makedirs(DATABASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        conn.commit()


def create_user(username, email, password_hash):
    with get_db_connection() as conn:
        conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash),
        )
        conn.commit()


def get_user_by_identifier(identifier):
    with get_db_connection() as conn:
        return conn.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?',
            (identifier, identifier.lower()),
        ).fetchone()
