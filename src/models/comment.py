from dataclasses import dataclass
from models.user import User


@dataclass
class Comment:
    """
    Represents a comment made by a user in the application.

    Attributes:
        id (int): Unique identifier for the comment.
        content (str): Text content of the comment.
        user (User): The user who authored the comment.
    """

    id: int
    content: str
    user: User
