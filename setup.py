import json
import secrets
import sqlite3

with open("config.json", "w") as file:
    config = {
        "CSRF_SECRET": secrets.token_urlsafe(32),
    }
    json.dump(config, file)

with open("init.sql") as file:
    db_init_script = file.read()

with sqlite3.connect("database.db") as db:
    cursor = db.cursor()
    cursor.executescript(db_init_script)
        
