from dataclasses import dataclass


@dataclass
class Tag:
    """
    Represents a tag with a unique identifier and a label.

    Attributes:
        id (int): A unique identifier of the tag.
        label (str): The descriptive name or label of the tag.
    """

    id: int
    label: str
