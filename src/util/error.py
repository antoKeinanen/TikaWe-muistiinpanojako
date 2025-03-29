import flask


def flash_errors(errors: list[str] | str, page_name: str, **url_values: dict[str, str]):
    """
    Flashes error messages to the user and redirects to a specified page.

    Args:
        errors (list[str] | str): A list of error messages or a single error message
        to be flashed.
        page_name (str): The name of the page to redirect to.
        **url_values (dict[str, str]): Additional URL values for the redirect.

    Returns:
        Response: A response object that redirects to the specified page.
    """

    if not isinstance(errors, list):
        errors = [errors]

    for error in errors:
        flask.flash(error, category="error")
    return flask.redirect(flask.url_for(page_name, **url_values))
