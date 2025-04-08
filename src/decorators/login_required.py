from functools import wraps
import flask
from collections.abc import Callable
from services import user_service
from util.logger import Logger


def login_required(f: Callable):
    """
    Ensure that a user is logged in before accessing a route.

    This decorator checks for an authorization token in the cookies.
    - If the token is missing or invalid, the user is redirected to the sign-in page.
    - If the token is valid, the user information is attached to the request object and
    the original function is executed.

    Args:
        f (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function that includes the login check.
    """

    @wraps(f)
    def decorated_function(*args: tuple, **kwargs: dict) -> flask.Response:
        token = flask.request.cookies.get("Authorization")
        if not token:
            flask.session["signed_in"] = False
            return flask.redirect(flask.url_for("signin_page", next=flask.request.url))

        user, error = user_service.get_user_by_token(token)
        if error:
            flask.session["signed_in"] = False
            Logger.error("Login required decorator failed to get user by token:", error)
            return flask.redirect(flask.url_for("signin_page", next=flask.request.url))

        flask.request.user = user
        flask.session["signed_in"] = True

        return f(*args, **kwargs)

    return decorated_function
