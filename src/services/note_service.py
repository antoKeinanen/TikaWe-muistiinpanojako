import util.database as db
from util.logger import Logger
import sqlite3
from models.note import Note
from models.user import User


def create_note(title: str, content: str, user_id: str):
    sql_command = """
    INSERT
    INTO notes (title, content, user_id)
    VALUES (?, ?, ?);
    """

    try:
        note_id = db.db_execute(sql_command, [title, content, user_id])
        new_note, error = get_note_by_id(note_id)
        return new_note, error

    except sqlite3.Error as er:
        Logger.error("Failed to create new note: ", er)
        return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"


def get_note_by_id(note_id: int, *, join_user: bool = False):
    sql_command = """
    SELECT id, title, content, user_id
    FROM notes
    WHERE id = ?;
    """

    if join_user:
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

    try:
        note = db.db_fetch(sql_command, [note_id])
        if not len(note):
            return None, "Muistiinpanoa ei löydetty"

        note = note[0]
        user = None
        if join_user:
            user = tuple(note[3:5])
            note = note[0:4]
            user = User(*user)

        return Note(*note, user), None

    except sqlite3.Error as er:
        Logger.error("Failed to create new note: ", er)
        return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"


def update_note_by_id(note_id: int, title: str, content: str):
    sql_command = """
    UPDATE notes
    SET
        title = ?,
        content = ?
    WHERE id = ?;
    """

    try:
        db.db_execute(sql_command, [title, content, note_id])
        return None, None
    except sqlite3.Error as er:
        Logger.error("Failed to delete note:", er)
        return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"


def delete_note_by_id(note_id: int):
    sql_command = "DELETE FROM notes WHERE id = ?"

    try:
        db.db_execute(sql_command, [note_id])
        return None, None
    except sqlite3.Error as er:
        Logger.error("Failed to update note:", er)
        return None, "Odottamaton virhe tapahtui. Yritä myöhemmin uudelleen!"


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

    try:
        notes = [Note(*note) for note in db.db_fetch_all(sql_command, [limit, offset])]
        return notes, None
    except sqlite3.Error as er:
        Logger.error("Failed to get latest notes: ", er)
        return [], "Odottamaton virhe tapahtui, Yritä myöhemmin uudelleen!"


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

    try:
        notes = [
            Note(*note)
            for note in db.db_fetch_all(sql_command, [f"%{query}%", limit, offset])
        ]
        return notes, None
    except sqlite3.Error as er:
        Logger.error("Failed to get notes by search query: ", er)
        return [], "Odottamaton virhe tapahtui, Yritä myöhemmin uudelleen!"
