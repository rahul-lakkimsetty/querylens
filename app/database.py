import sqlite3
from flask import current_app

def get_db_connection():
    """Establish a connection to the SQLite database configured in Flask app config."""
    db_path = current_app.config["DATABASE_PATH"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_schema_info():
    """
    Retrieve database schema catalog.
    Queries the SQLite system tables for tables, column names, and data types
    to compile details for LLM context injection.
    """
    schema = {}
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all non-system tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row["name"] for row in cursor.fetchall()]
        
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns_data = cursor.fetchall()
            schema[table] = [
                {
                    "name": col["name"],
                    "type": col["type"],
                    "primary_key": bool(col["pk"])
                }
                for col in columns_data
            ]
        conn.close()
    except sqlite3.Error as e:
        # Gracefully handle database access issues (e.g. if database file doesn't exist yet)
        current_app.logger.warning(f"Database schema retrieval warning: {e}")
    return schema

def execute_select_query(sql_query):
    """
    Execute a SELECT query safely on the database and return results as a list of dicts.
    Note: Real security validation happens in core.validation (SQLGlot).
    """
    results = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        for row in rows:
            results.append(dict(row))
        conn.close()
    except sqlite3.Error as e:
        raise e
    return results
