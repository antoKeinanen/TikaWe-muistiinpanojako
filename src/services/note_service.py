import util.database as db
from models.note import Note
from models.user import User


def create_note(title: str, content: str, user_id: str):
    sql_command = """
    INSERT
    INTO notes (title, content, user_id)
    VALUES (?, ?, ?);
    """

    return db.db_execute(sql_command, [title, content, user_id])


def get_note_by_id(note_id: int):
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
    if not len(note_data):
        return None, "Muistiinpanoa ei löydetty"

    note_data = note_data[0]
    user = User(*note_data[3:5])

    return Note(*note_data[0:4], user), None


def update_note_by_id(note_id: int, title: str, content: str):
    sql_command = """
    UPDATE notes
    SET
        title = ?,
        content = ?
    WHERE id = ?;
    """

    db.db_execute(sql_command, [title, content, note_id])


def delete_note_by_id(note_id: int):
    sql_command = "DELETE FROM notes WHERE id = ?"

    db.db_execute(sql_command, [note_id])


def get_recent_notes(limit: int = 10, offset: int = 0):
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
