class User:
    def __init__(self, user_id: int, username: str, password_hash: str) -> None:
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
