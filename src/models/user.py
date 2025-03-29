from dataclasses import dataclass


@dataclass
class User:
    """
    Data class representing a User entity.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        password_hash (str, optional): The hashed password of the user. Defaults to None.
        token (str, optional): The authentication token for the user. Defaults to None.
    """  # noqa: E501

    id: int
    username: str
    password_hash: str | None = None
    token: str | None = None
