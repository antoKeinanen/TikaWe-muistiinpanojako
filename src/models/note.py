from dataclasses import dataclass
from models.user import User


@dataclass
class Note:
    id: int
    title: str
    content: str
    user_id: str
    user: User | None = None
