import flask


def inject_errors() -> dict:
    """
    Retrieve flashed error messages from the Flask session and prepare them for
    injection into templates.

    This function collects error messages that have been flashed with the category
    `"error"` and returns them in a dictionary along with the count of errors.

    Returned value is automatically injected for usage in jinja templates.

    Returns:
        dict: A dictionary containing enumerated error messages and the count of errors.
    """

    errors = flask.get_flashed_messages(category_filter="error")
    return {"errors": enumerate(errors), "error_count": len(errors)}
