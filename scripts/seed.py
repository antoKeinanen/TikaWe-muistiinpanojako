from pathlib import Path
import json
import secrets
import sqlite3
from util.sanalista import sanalista
from util.nimet import etunimet, sukunimet
import itertools
import random

random.seed(200)

USER_COUNT = 100_000
NOTE_COUNT = USER_COUNT * 5
TAG_COUNT = NOTE_COUNT * 3
COMMENT_COUNT = NOTE_COUNT * 5

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

    all_names = itertools.product(etunimet, sukunimet)
    all_names = [e + s for e, s in all_names]

    if len(all_names) < USER_COUNT:
        msg = f"Maksimi määrä käyttäjiä on {len(all_names)}"
        raise ValueError(msg)

    usernames = random.sample(all_names, USER_COUNT)
    passwords = [secrets.token_urlsafe(32) for _ in range(USER_COUNT)]
    tokens = [secrets.token_urlsafe(32) for _ in range(USER_COUNT)]

    cursor.executemany(
        "INSERT INTO users (username, password_hash, token) VALUES (?, ?, ?)",
        zip(usernames, passwords, tokens, strict=False),
    )

    notes = []
    for _ in range(NOTE_COUNT):
        user_id = random.randint(1, USER_COUNT)
        num_words = random.randint(5, 15)
        title = " ".join(random.choices(sanalista, k=2))
        content = " ".join(random.choices(sanalista, k=num_words))
        notes.append((user_id, content, title))

    cursor.executemany(
        "INSERT INTO notes (user_id, content, title) VALUES (?, ?, ?)",
        notes,
    )

    tags = []
    for note_id in range(1, NOTE_COUNT + 1):
        for _ in range(3):
            label = random.choice(sanalista)
            tags.append((note_id, label))
    cursor.executemany(
        "INSERT INTO tags (note_id, label) VALUES (?, ?)",
        tags,
    )

    comments = []
    for _ in range(COMMENT_COUNT):
        user_id = random.randint(1, USER_COUNT)
        note_id = random.randint(1, NOTE_COUNT)
        num_words = random.randint(3, 20)
        content = " ".join(random.choices(sanalista, k=num_words))
        comments.append((user_id, note_id, content))

    cursor.executemany(
        "INSERT INTO comments (user_id, note_id, content) VALUES (?, ?, ?)",
        comments,
    )
