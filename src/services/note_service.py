import util.database as db
from models.note import Note
from models.user import User


def create_note(title: str, content: str, user_id: str):
    """
    Create a new note with the given title, content, and user ID.

    Args:
        title (str): The title of the note.
        content (str): The content of the note.
        user_id (str): The ID of the user creating the note.

    Returns:
        int (optional): The last affected row id
    """

    sql_command = """
    INSERT
    INTO notes (title, content, user_id)
    VALUES (?, ?, ?);
    """

    return db.db_execute(sql_command, [title, content, user_id])


def get_note_by_id(note_id: int):
    """
    Retrieve a note by its ID.

    Args:
        note_id (int): The ID of the note to retrieve.

    Returns:
        tuple: An errors as value tuple containing either the note or an error message.
    """

    sql_command = """
        SELECT
            notes.id AS note_id,
            notes.title,
            notes.content,
            users.id AS user_id,
            users.username
        FROM notes
        JOIN users ON notes.user_id = users.id
        WHERE notes.id = ?;
    """

    note_data = db.db_fetch(sql_command, [note_id])
    if not note_data:
        return None, "Muistiinpanoa ei löydetty"

    note_data = note_data[0]
    user = User(*note_data[3:5])

    return Note(*note_data[0:4], user), None


def update_note_by_id(note_id: int, title: str, content: str):
    """
    Update the title and content of a note by its ID.

    Args:
        note_id (int): The ID of the note to update.
        title (str): The new title of the note.
        content (str): The new content of the note.
    """

    sql_command = """
    UPDATE notes
    SET
        title = ?,
        content = ?
    WHERE id = ?;
    """

    db.db_execute(sql_command, [title, content, note_id])


def delete_note_by_id(note_id: int):
    """
    Delete a note by its ID.

    Args:
        note_id (int): The ID of the note to delete.
    """

    sql_command = "DELETE FROM notes WHERE id = ?"

    db.db_execute(sql_command, [note_id])


def get_recent_notes(limit: int = 10, offset: int = 0):
    """
    Retrieve recent notes with pagination.

    Args:
        limit (int, optional): The maximum number of notes to retrieve. Defaults to 10.
        offset (int, optional): The number of notes to skip before starting to retrieve. Defaults to 0.

    Returns:
        list: A list of Note objects.
    """  # noqa: E501

    sql_command = """
    SELECT
        notes.id AS note_id,
        notes.title,
        notes.content,
        users.id AS user_id,
        users.username
    FROM notes
    JOIN users ON notes.user_id = users.id
    ORDER BY notes.created_at DESC
    LIMIT ?
    OFFSET ?
    """

    notes = db.db_fetch_all(sql_command, [limit, offset])
    return [Note(*note) for note in notes]


def get_note_by_query(query: str, limit: int = 10, offset: int = 0):
    """
    Retrieve notes by a search query with pagination.

    Args:
        query (str): The search query to filter notes by title.
        limit (int, optional): The maximum number of notes to retrieve. Defaults to 10.
        offset (int, optional): The number of notes to skip before starting to retrieve. Defaults to 0.

    Returns:
        list: A list of Note objects.
    """  # noqa: E501

    sql_command = """
    SELECT
        notes.id AS note_id,
        notes.title,
        notes.content,
        users.id AS user_id,
        users.username
    FROM notes
    JOIN users ON notes.user_id = users.id
    WHERE notes.title
        LIKE ?
    ORDER BY notes.created_at DESC
    LIMIT ?
    OFFSET ?
    """

    notes = db.db_fetch_all(sql_command, [f"%{query}%", limit, offset])
    return [Note(*note) for note in notes]


def get_notes_by_user(user: User):
    """
    Get all note records associated with the given user.

    Arguments:
        user (User): The user for whom the notes are to be retrieved.
            The user object must have an 'id' attribute.

    Returns:
        List[Note]: A list of Note objects corresponding to the notes belonging to the
            specified user.
    """

    sql_command = """
    SELECT id, title, content, user_id
    FROM notes
    WHERE user_id = ?;
    """

    notes = db.db_fetch_all(sql_command, [user.id])
    return [Note(*note, user=user) for note in notes]
