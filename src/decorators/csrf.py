from functools import wraps
import secrets
import flask
from collections.abc import Callable
from util.logger import Logger
from util.config import config


def setup(f: Callable):
    """
    Set up CSRF protection by generating a CSRF token and storing it in the
    Flask session before calling the decorated function.

    Should be used as pairs with csrf.setup on the page and csrf.validate on the action.

    Args:
        f (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function that includes CSRF token setup.

    Example:
        ```python
        @csrf.setup
        def my_view_function():
            # Your view logic here
            return flask.Response("Hello, World!")
        ```
    """

    @wraps(f)
    def decorated_function(*args: tuple, **kwargs: dict) -> flask.Response:
        if config.csrf_enabled:
            flask.session["csrf_token"] = secrets.token_hex(16)

        return f(*args, **kwargs)

    return decorated_function


def validate(fallback: str = "index_page"):
    """
    Validate the CSRF token from the client against the server's stored CSRF token
    before executing the decorated function.

    Should be used as pairs with csrf.setup on the page and csrf.validate on the action.

    Args:
        fallback (str, optional): The name of the fallback route to redirect to in case
        of validation failure. Defaults to `"index_page"`.

    Returns:
        Callable: The decorated function that includes CSRF token validation.

    Example:
        ```python
        @csrf.validate(fallback="home_page")
        def my_secure_action():
            # Your secure view logic here
            return flask.Response("Secure Content")
        ```
    """

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: tuple, **kwargs: dict) -> flask.Response:
            if not config.csrf_enabled:
                return f(*args, **kwargs)

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
