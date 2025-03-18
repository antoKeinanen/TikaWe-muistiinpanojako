from functools import wraps
import flask
from collections.abc import Callable
from services import auth_service
from util.logger import Logger


def login_required(f: Callable):
    @wraps(f)
    def decorated_function(*args: tuple, **kwargs: dict) -> flask.Response:
        token = flask.session.get("token")
        if not token:
            return flask.redirect(flask.url_for("signin_page", next=flask.request.url))

        user, error = auth_service.get_user_by_token(token)
        if error:
            Logger.error("Login required decorator failed to get user by token:", error)
            return flask.redirect(flask.url_for("signin_page", next=flask.request.url))

        args = (user, *args)
        return f(*args, **kwargs)

    return decorated_function
