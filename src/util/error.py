import flask


def flash_errors(errors: list[str] | str, page_name: str, **url_values: dict[str, str]):
    if not isinstance(errors, list):
        errors = [errors]

    for error in errors:
        flask.flash(error, category="error")
    return flask.redirect(flask.url_for(page_name, **url_values))
