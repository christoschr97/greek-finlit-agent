"""
Database connection and utilities.
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """Get a database connection."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "finlit_db"),
        user=os.getenv("DB_USER", "finlit_user"),
        password=os.getenv("DB_PASSWORD", "finlit_password"),
        cursor_factory=RealDictCursor
    )


def check_db_connection():
    """Check if database connection is working."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
                return result["test"] == 1
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def init_db():
    """Initialize database tables if they don't exist."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Create a simple users table for demonstration
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100) UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
