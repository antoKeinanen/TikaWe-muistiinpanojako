import util.database as db
from models.note import Note
from models.user import User
from models.tag import Tag


def create_note(title: str, content: str, user_id: str, tags: list[str]):
    """
    Create a new note with the given title, content, and user ID.

    Args:
        title (str): The title of the note.
        content (str): The content of the note.
        user_id (str): The ID of the user creating the note.
        tags (list[str]): The list of tags associated with the note.

    Returns:
        int (optional): The last affected row id
    """

    sql_command = """
    INSERT
    INTO notes (title, content, user_id)
    VALUES (?, ?, ?);
    """

    note_id = db.db_execute(sql_command, [title, content, user_id])

    sql_command = """
    INSERT
    INTO tags (label, note_id)
    VALUES (?, ?);
    """

    for tag in tags:
        db.db_execute(sql_command, [tag, note_id])

    return note_id


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


def update_note_by_id(note_id: int, title: str, content: str, tags: list[str]):
    """
    Update the title and content of a note by its ID.

    Args:
        note_id (int): The ID of the note to update.
        title (str): The new title of the note.
        content (str): The new content of the note.
        tags (list[str]): List of tags associated with the post.
    """

    sql_command = """
    UPDATE notes
    SET
        title = ?,
        content = ?
    WHERE id = ?;
    """
    db.db_execute(sql_command, [title, content, note_id])

    sql_command = """
    DELETE FROM tags
    WHERE note_id = ?;
    """
    db.db_execute(sql_command, [note_id])

    sql_command = """
    INSERT
    INTO tags (label, note_id)
    VALUES (?, ?);
    """
    for tag in tags:
        db.db_execute(sql_command, [tag, note_id])


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
        tuple: A tuple containing a list of Note objects and the total count of notes.
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

    sql_command = "SELECT COUNT(*) FROM notes"
    note_count = db.db_fetch(sql_command, [])
    note_count = note_count[0][0]

    return [Note(*note) for note in notes], note_count


def get_note_by_query(query: str, limit: int = 10, offset: int = 0):
    """
    Retrieve notes by a search query with pagination.

    Args:
        query (str): The search query to filter notes by title.
        limit (int, optional): The maximum number of notes to retrieve. Defaults to 10.
        offset (int, optional): The number of notes to skip before starting to retrieve.
            Defaults to 0.

    Returns:
        list: A list of Note objects.
    """

    sql_command = """
    SELECT DISTINCT
        notes.id AS note_id,
        notes.title,
        notes.content,
        users.id AS user_id,
        users.username
    FROM notes
    JOIN users ON notes.user_id = users.id
    JOIN tags ON notes.id = tags.note_id
    WHERE notes.title LIKE ?
        OR tags.label LIKE ?
    ORDER BY notes.created_at DESC
    LIMIT ?
    OFFSET ?
    """

    query = f"%{query}%"

    notes = db.db_fetch_all(sql_command, [query, query, limit, offset])

    sql_command = """
    SELECT count(DISTINCT notes.id)
    FROM notes
    JOIN tags ON notes.id = tags.note_id
    WHERE
        notes.title LIKE ?
        OR tags.label LIKE ?
    """
    note_count = db.db_fetch(sql_command, [query, query])
    note_count = note_count[0][0]

    return [Note(*note) for note in notes], note_count


def get_notes_by_user(user: User, limit: int = 10, offset: int = 0):
    """
    Get all note records associated with the given user.

    Arguments:
        user (User): The user for whom the notes are to be retrieved.
            The user object must have an 'id' attribute.
        limit (int, optional): The maximum number of notes to retrieve. Defaults to 10.
        offset (int, optional): The number of notes to skip before starting to retrieve.
            Defaults to 0.

    Returns:
        List[Note]: A list of Note objects corresponding to the notes belonging to the
            specified user.
    """

    sql_command = """
    SELECT id, title, content, user_id
    FROM notes
    WHERE user_id = ?
    ORDER BY created_at DESC
    LIMIT ?
    OFFSET ?
    """

    notes = db.db_fetch_all(sql_command, [user.id, limit, offset])
    return [Note(*note, user=user) for note in notes]


def get_tags_by_note(note: Note):
    """
    Retrieve all tags associated with the specified note.

    Arguments:
        note (Note): The note object for which to retrieve tags.

    Returns:
        List[Tag]: A list of Tag objects corresponding to the tags associated
            with the note.
    """

    sql_command = """
    SELECT id, label
    FROM tags
    WHERE note_id = ?;
    """

    tags = db.db_fetch_all(sql_command, [note.id])
    return [Tag(*tag) for tag in tags]
