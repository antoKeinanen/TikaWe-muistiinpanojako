from dataclasses import dataclass


@dataclass
class Pagination:
    """
    Pagination class represents a pagination component with navigation arrows,
    an active page, and a list of page numbers.

    Args:
        left_arrow (bool): Indicates if the left navigation arrow is visible.
        right_arrow (bool): Indicates if the right navigation arrow is visible.
        active_page (str): The currently active page.
        numbers (list[str]): A list of page numbers as strings.
    """

    left_arrow: bool
    right_arrow: bool
    active_page: str
    numbers: list[str]
