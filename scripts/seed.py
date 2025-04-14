from pathlib import Path
import json
import secrets
import sqlite3
from util.sanalista import sanalista
import random

random.seed(200)

USER_COUNT = 1_000_000
NOTE_COUNT = 5_000_000
TAG_COUNT = 3_000_000
COMMENT_COUNT = 15_000_000

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

    for i in range(USER_COUNT):
        if i % (USER_COUNT // 10) == 0:
            print(f"{i}/{USER_COUNT} users added")  # noqa: T201
        password = secrets.token_urlsafe(32)
        token = secrets.token_urlsafe(32)
        cursor.execute(
            "INSERT INTO users (username, password_hash, token) VALUES (?, ?, ?)",
            (f"Käyttäjä{i}", password, token),
        )

    for _ in range(NOTE_COUNT):
        if i % (NOTE_COUNT // 10) == 0:
            print(f"{i}/{NOTE_COUNT} notes added")  # noqa: T201
        user_id = random.randint(1, USER_COUNT)
        num_words = random.randint(5, 15)
        title = " ".join(random.choices(sanalista, k=2))
        content = " ".join(random.choices(sanalista, k=num_words))
        cursor.execute(
            "INSERT INTO notes (user_id, content, title) VALUES (?, ?, ?)",
            (user_id, content, title),
        )

    for i in range(TAG_COUNT):
        if i % (TAG_COUNT // 10) == 0:
            print(f"{i}/{TAG_COUNT} tags added")  # noqa: T201
        note_id = random.randint(1, NOTE_COUNT)
        label = random.choice(sanalista)
        cursor.execute(
            "INSERT INTO tags (note_id, label) VALUES (?, ?)",
            (note_id, label),
        )

    for i in range(COMMENT_COUNT):
        if i % (COMMENT_COUNT // 10) == 0:
            print(f"{i}/{COMMENT_COUNT} comments added")  # noqa: T201
        user_id = random.randint(1, USER_COUNT)
        note_id = random.randint(1, NOTE_COUNT)
        num_words = random.randint(3, 20)
        content = " ".join(random.choices(sanalista, k=num_words))
        cursor.execute(
            "INSERT INTO comments (user_id, note_id, content) VALUES (?, ?, ?)",
            (user_id, note_id, content),
        )
