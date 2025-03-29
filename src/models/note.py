from dataclasses import dataclass
from models.user import User


@dataclass
class Note:
    """
    Data class representing a Note entity.

    Attributes:
        id (int): The unique identifier of the note.
        title (str): The title of the note.
        content (str): The content of the note.
        user_id (str): The unique identifier of the user who created the note.
        user (User, optional): The user object associated with the note. Defaults to None.
    """  # noqa: E501

    id: int
    title: str
    content: str
    user_id: str
    user: User | None = None
