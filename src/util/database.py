import sqlite3
from sqlite3 import Cursor
from collections.abc import Callable
from typing import Any


def _perform_db_operation(action: Callable[[Cursor], Any]):
    """
    Execute a database operation within a managed SQLite connection.

    Args:
        action (Callable[[sqlite3.Cursor], Any]):
            A callable that takes a single argument,
            a SQLite cursor, performs a database operation, and returns a result.

    Returns:
        Any: The result returned by the 'action' callable.
    """

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        return action(cursor)


def db_execute(sql_command: str, arguments: list | None = None):
    """
    Execute a given SQL command on the 'database.db' and returns the ID of the
    last row affected.

    Args:
        sql_command (str): The SQL command to be executed.
        arguments (list | None, optional): A list of arguments to be passed to
        the SQL command. Defaults to None.

    Returns:
        int: The ID of the last row affected by the SQL command.
    """

    def execute(cursor: Cursor):
        return cursor.execute(sql_command, arguments).lastrowid

    return _perform_db_operation(execute)


def db_fetch(sql_command: str, arguments: list | None = None, size: int = 1):
    """
    Fetch a specified number of rows from the result of a given SQL command
    executed on 'database.db'.

    Args:
        sql_command (str): The SQL command to be executed.
        arguments (list | None, optional): A list of arguments to be passed to
        the SQL command. Defaults to None.
        size (int, optional): The number of rows to fetch. Defaults to 1.

    Returns:
        list: A list of fetched rows.
    """

    def fetch(cursor: Cursor):
        cursor.execute(sql_command, arguments)
        return cursor.fetchmany(size)

    return _perform_db_operation(fetch)


def db_fetch_all(sql_command: str, arguments: list | None = None):
    """
    Fetch all rows from the result of a given SQL command executed on 'database.db'.

    Args:
        sql_command (str): The SQL command to be executed.
        arguments (list | None, optional): A list of arguments to be passed to
        the SQL command. Defaults to None.

    Returns:
        list: A list of all fetched rows.
    """

    def fetch_all(cursor: Cursor):
        cursor.execute(sql_command, arguments)
        return cursor.fetchall()

    return _perform_db_operation(fetch_all)
