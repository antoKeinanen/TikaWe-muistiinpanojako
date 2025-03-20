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
            return None, f"Could not find note by the id {note_id}"

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
