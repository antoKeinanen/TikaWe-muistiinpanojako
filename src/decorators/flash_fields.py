from functools import wraps
import flask
from collections.abc import Callable
import json


def flash_fields(f: Callable):
    @wraps(f)
    def decorated_function(*args: tuple, **kwargs: dict) -> flask.Response:
        fields = flask.request.form.to_dict()
        flask.flash(json.dumps(fields), category="fields")

        return f(*args, **kwargs)

    return decorated_function
