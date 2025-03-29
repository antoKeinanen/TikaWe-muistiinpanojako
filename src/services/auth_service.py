import sqlite3
from werkzeug.security import generate_password_hash
from models.user import User
import util.database as db
import secrets


def create_user(username: str, plain_password: str):
    """
    Create a new user with the given username and plain password.

    The function automatically hashes the password with `crypt:131072:8:1`
    and generates an access token for the user.

    Args:
        username (str): The username for the new user.
        plain_password (str): The plain text password for the new user.

    Returns:
        tuple: A tuple containing the User object and an error message.
               If the user is created successfully, error is None.
               If the username is already taken, returns None and an error message.
    """

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


def get_user_by_username(username: str):
    """
    Retrieve a user by their username.

    Args:
        username (str): The username of the user to retrieve.

    Returns:
        tuple: A tuple containing the User object and an error message.
               If the user is found, error is None.
               If the user is not found, returns None and an error message.
    """

    sql_command = """
    SELECT id, username, password_hash, token
    FROM users
    WHERE username = ?;
    """

    user = db.db_fetch(sql_command, [username])
    if not user:
        return None, "Virheellinen käyttäjätunnus ja/tai salasana"
    return User(*user[0]), None


def get_user_by_token(token: str):
    """
    Retrieve a user by their token.

    Args:
        token (str): The token of the user to retrieve.

    Returns:
        tuple: A tuple containing the User object and an error message.
               If the user is found, error is None.
               If the user is not found, returns None and an error message.
    """

    sql_command = """
    SELECT id, username, password_hash, token
    FROM users
    WHERE token = ?;
    """

    user = db.db_fetch(sql_command, [token])
    if not user:
        return None, "Token ei vastaa käyttäjää"
    return User(*user[0]), None
