import sqlite3
from src.utils.helpers import load_config


def get_db_connection(db_path: str = None) -> sqlite3.Connection:
    """
    Return a SQLite3 connection to the given database path.

    Args:
        db_path: Path to the SQLite database file. If None, uses config value.

    Returns:
        sqlite3.Connection: A connection object to the database
    """
    if db_path is None:
        config = load_config()
        db_path = config["database"]["path"]

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_jobs_table(conn: sqlite3.Connection) -> None:
    """
    Create the jobs table if it does not exist.

    Args:
        conn: SQLite3 connection object
    """
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            url TEXT NOT NULL,
            currency TEXT,
            salary TEXT,
            location TEXT,
            source TEXT NOT NULL,
            date_posted TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()


def init_db(db_path: str = None) -> sqlite3.Connection:
    """
    Initialize DB by creating connection and ensuring schema exists.

    Args:
        db_path: Path to the SQLite database file. If None, uses config value.

    Returns:
        sqlite3.Connection: A connection object to the initialized database
    """
    conn = get_db_connection(db_path)
    create_jobs_table(conn)
    return conn

