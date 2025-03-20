from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password_hash: str | None = None
    token: str | None = None
