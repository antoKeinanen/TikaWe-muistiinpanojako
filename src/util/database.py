import sqlite3


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

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(sql_command, arguments)
        return cursor.lastrowid


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

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(sql_command, arguments)
        return cursor.fetchmany(size)


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

    with sqlite3.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(sql_command, arguments)
        return cursor.fetchall()
