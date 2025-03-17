import sqlite3
from werkzeug.security import generate_password_hash


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
            return "Tunnus on jo varattu"
        except sqlite3.Error as ex:
            print(ex)
            return "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"
    return None
