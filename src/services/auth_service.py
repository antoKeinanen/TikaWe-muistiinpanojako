import sqlite3
from werkzeug.security import generate_password_hash
from models.user import User


def create_user(username: str, plain_password: str):
    password_hash = generate_password_hash(
        plain_password,
        method="scrypt:131072:8:1",
        salt_length=32,
    )
    with sqlite3.connect("database.db") as connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            cursor.execute(sql, [username, password_hash])
        except sqlite3.IntegrityError:
            return None, "Tunnus on jo varattu"
        except sqlite3.Error as ex:
            print(ex)
            return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"
    return None, None


def get_user(username: str):
    with sqlite3.connect("database.db") as connection:
        try:
            cursor = connection.cursor()
            sql = "SELECT id, username, password_hash FROM users WHERE username = ?"
            cursor.execute(sql, [username])
            user = cursor.fetchone()

            if not len(user):
                return None, "Virheellinen käyttäjätunnus ja/tai salasana"
            return User(*user), None
        except sqlite3.Error as ex:
            print(ex)
            return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"
