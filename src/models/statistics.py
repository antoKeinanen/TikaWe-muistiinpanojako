from dataclasses import dataclass


@dataclass
class Statistics:
    """Represents statistics for notes and comments."""

    note_count: int
    comment_count: int
