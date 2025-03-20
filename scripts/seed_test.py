from pathlib import Path
import sqlite3

with Path("scripts/sql/seed_test.sql").open() as file:
    seed_script = file.read()

with sqlite3.connect("database.db") as connection:
    cursor = connection.cursor()
    cursor.executescript(seed_script)
