from pathlib import Path
import json
import secrets
import sqlite3

Path("config.json").unlink(missing_ok=True)

with open("config.json", "w") as file:
    config = {
        "CSRF_SECRET": secrets.token_urlsafe(32),
    }
    json.dump(config, file)

with open("scripts/sql/init.sql") as file:
    db_init_script = file.read()

Path("database.db").unlink(missing_ok=True)

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    cursor.executescript(db_init_script)
