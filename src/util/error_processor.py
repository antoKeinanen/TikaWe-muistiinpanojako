import flask


def inject_errors() -> dict:
    errors = flask.get_flashed_messages(category_filter="error")
    return {"errors": enumerate(errors), "error_count": len(errors)}
