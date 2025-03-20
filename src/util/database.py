import sqlite3


def db_execute(sql_command: str, arguments: list | None = None):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(sql_command, arguments)
        return cursor.lastrowid


def db_fetch(sql_command: str, arguments: list | None = None, size: int = 1):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(sql_command, arguments)
        return cursor.fetchmany(size)


def db_fetch_all(sql_command: str, arguments: list | None = None):
    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(sql_command, arguments)
        return cursor.fetchall()
