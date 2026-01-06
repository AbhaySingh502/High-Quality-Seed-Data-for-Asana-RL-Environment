import sqlite3
import os

DB_PATH = "output/asana_simulation.sqlite"


def run_schema(schema_path="schema.sql", db_path=DB_PATH):
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Delete old DB BEFORE opening connection
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create fresh connection
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")

    # Run schema
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    return conn
