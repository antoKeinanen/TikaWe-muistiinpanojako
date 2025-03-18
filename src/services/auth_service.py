import sqlite3
from werkzeug.security import generate_password_hash
from models.user import User
import util.database as db


def create_user(username: str, plain_password: str):
    password_hash = generate_password_hash(
        plain_password,
        method="scrypt:131072:8:1",
        salt_length=32,
    )

    try:
        sql_command = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.db_execute(sql_command, [username, password_hash])
        return None, None
    except sqlite3.IntegrityError:
        return None, "Käyttäjätunnus on jo varattu"
    except sqlite3.Error as er:
        print(er)
        return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"


def get_user(username: str):
    try:
        sql_command = """
        SELECT id, username, password_hash
        FROM users
        WHERE username = ?;
        """
        user = db.db_fetch(sql_command, [username])
        if not len(user):
            return None, "Virheellinen käyttäjätunnus ja/tai salasana"
        return User(*user[0]), None
    except sqlite3.Error as er:
        print(er)
        return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"
