import util.database as db
from models.user import User
from models.comment import Comment


def create_comment(content: str, user_id: int, note_id: int):
    """
    Create a comment in the database.

    Args:
        content (str): The content of the comment.
        user_id (int): The ID of the user creating the comment.
        note_id (int): The ID of the note that the comment is created under.
    """

    sql_command = """
    INSERT INTO comments (content, user_id, note_id)
    VALUES (?, ?, ?);
    """

    db.db_execute(sql_command, [content, user_id, note_id])


def get_note_comments(note_id: int):
    """
    Retrieve all comments associated with a specified note,
    along with the user details for each comment.

    Args:
        note_id (int): The ID of the note for which comments are to be retrieved.

    Returns:
        List[Comment]: A list of Comment objects.
    """

    sql_command = """
    SELECT
        comments.id,
        comments.content,
        users.id,
        users.username
    FROM comments
    JOIN users ON users.id = comments.user_id
    WHERE comments.note_id = ?
    ORDER BY comments.created_at DESC;
    """

    data = db.db_fetch_all(sql_command, [note_id])
    users = [User(*d[2:4]) for d in data]
    comment_data = [d[0:2] for d in data]

    return [
        Comment(*comment, user=user)
        for comment, user in zip(comment_data, users, strict=True)
    ]
