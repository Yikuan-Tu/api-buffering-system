import sqlite3
import logging
from typing import List, Tuple
from app.utils.config import DB_PATH

logger = logging.getLogger(__name__)


def init_db():
    db_connection = get_connection()
    cursor = db_connection.cursor()

    cursor.execute(
        """
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='people'
    """
    )

    if cursor.fetchone():
        logger.info("Database already initialized")
    else:
        logger.info("Initializing database...")

        cursor.execute(
            """
            CREATE TABLE people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        db_connection.commit()
        logger.info("✅ Database initialized")
    db_connection.close()


def get_connection():
    return sqlite3.connect(str(DB_PATH))


def execute_query(query: str, params: Tuple = ()):
    # Execute a single query
    db_connection = get_connection()
    try:
        cursor = db_connection.cursor()
        cursor.execute(query, params)
        db_connection.commit()
        return cursor.fetchone()[0]
    finally:
        db_connection.close()


def batch_insert(records: List[Tuple[str, str]]):
    db_connection = get_connection()
    try:
        cursor = db_connection.cursor()
        cursor.executemany(
            "INSERT INTO people (first_name, last_name) VALUES (?, ?)", records
        )
        db_connection.commit()
        return cursor.rowcount
    except Exception as e:
        db_connection.rollback()
        raise e
    finally:
        db_connection.close()
