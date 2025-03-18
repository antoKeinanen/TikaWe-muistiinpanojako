from functools import wraps
import secrets
import flask
from collections.abc import Callable
from util.logger import Logger


def setup(f: Callable):
    @wraps(f)
    def decorated_function(*args: tuple, **kwargs: dict) -> flask.Response:
        flask.session["csrf_token"] = secrets.token_hex(16)

        return f(*args, **kwargs)

    return decorated_function


def validate(fallback: str):
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: tuple, **kwargs: dict) -> flask.Response:
            client_csrf_token = flask.request.form.get("csrf_token")
            server_csrf_token = flask.session.get("csrf_token")

            if not client_csrf_token or not server_csrf_token:
                Logger.error("no token found")
                flask.flash("CSRF token puuttuu", category="error")
                return flask.redirect(flask.url_for(fallback))

            if client_csrf_token != server_csrf_token:
                Logger.error("tokens do not match")
                flask.flash("CSRF tokenin validointi virhe", category="error")
                return flask.redirect(flask.url_for(fallback))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
