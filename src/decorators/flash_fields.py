from functools import wraps
import flask
from collections.abc import Callable
import json


def flash_fields(f: Callable):
    """
    Flash form fields from a Flask request before calling the decorated function.

    The flashed fields are then read automatically by the `inject_fields` injector and
    injected for usage in jinja templates.

    Args:
        f (Callable): The function to be decorated. This function should accept a Flask
        request and return a Flask response.

    Returns:
        Callable: The decorated function which flashes form fields before executing the
        original function.
    """

    @wraps(f)
    def decorated_function(*args: tuple, **kwargs: dict) -> flask.Response:
        fields = flask.request.form.to_dict()
        flask.flash(json.dumps(fields), category="fields")

        return f(*args, **kwargs)

    return decorated_function
