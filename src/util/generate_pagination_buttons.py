from models.pagination import Pagination


def _generate_numbers(page: int, page_count: int):
    """
    Generate a list of pagination button labels based on the current page and total page
    count.

    Args:
        page (int): The current page number (1-based index).
        page_count (int): The total number of pages.

    Returns:
        list: A list of strings and/or integers representing the pagination buttons.
              The list includes page numbers and ellipses ("...") where appropriate.
    """
    if page_count <= 5:
        return [str(n) for n in range(1, page_count + 1)]
    if page < 5:
        return [*(range(1, 6)), "...", page_count]
    if page > page_count - 3:
        return [1, "...", *(range(page_count - 4, page_count + 1))]
    return [1, "...", page - 1, page, page + 1, "...", page_count]


def generate_pagination_buttons(page: int, page_count: int):
    """
    Generate pagination button data for a given page and total page count.

    Args:
        page (int): The current page number (1-based index).
        page_count (int): The total number of pages.

    Returns:
        Pagination: An object containing the following attributes:
            - left_arrow (bool): Indicates if the left arrow button should be enabled.
            - right_arrow (bool): Indicates if the right arrow button should be enabled.
            - active_page (str): The current page number as a string.
            - numbers (list of str): A list of page numbers to display as strings.
    """
    left_arrow = page > 1
    right_arrow = page < page_count
    active_page = str(page)
    numbers = [str(n) for n in _generate_numbers(page, page_count)]

    return Pagination(left_arrow, right_arrow, active_page, numbers)
