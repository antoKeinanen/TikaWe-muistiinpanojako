import sqlite3
from werkzeug.security import generate_password_hash
from models.user import User
import util.database as db
from util.logger import Logger
import secrets


def create_user(username: str, plain_password: str):
    password_hash = generate_password_hash(
        plain_password,
        method="scrypt:131072:8:1",
        salt_length=32,
    )
    token = secrets.token_urlsafe(32)

    sql_command = """
    INSERT
    INTO users (username, password_hash, token)
    VALUES (?, ?, ?);
    """

    try:
        db.db_execute(sql_command, [username, password_hash, token])
        user, error = get_user_by_username(username)
        return user, error

    except sqlite3.IntegrityError:
        return None, "Käyttäjätunnus on jo varattu"

    except sqlite3.Error as er:
        Logger.error("Error creating user:", er)
        return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"


def get_user_by_username(username: str):
    sql_command = """
    SELECT id, username, password_hash, token
    FROM users
    WHERE username = ?;
    """

    try:
        user = db.db_fetch(sql_command, [username])
        if not len(user):
            return None, "Virheellinen käyttäjätunnus ja/tai salasana"
        return User(*user[0]), None

    except sqlite3.Error as er:
        Logger.error("Error getting user:", er)
        return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"


def get_user_by_token(token: str):
    sql_command = """
    SELECT id, username, password_hash, token
    FROM users
    WHERE token = ?;
    """

    try:
        user = db.db_fetch(sql_command, [token])
        if not len(user):
            return None, "Invalid token"
        return User(*user[0]), None

    except sqlite3.Error as er:
        return None, str(er)
