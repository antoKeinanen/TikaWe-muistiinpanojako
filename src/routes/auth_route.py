import secrets
import flask
from services import auth_service
from werkzeug.security import check_password_hash


def signin_page():
    errors = flask.get_flashed_messages(category_filter="error")
    flask.session["csrf_token"] = secrets.token_hex(16)
    return flask.render_template("signin.html", errors=enumerate(errors))


def signup_page():
    errors = flask.get_flashed_messages(category_filter="error")
    flask.session["csrf_token"] = secrets.token_hex(16)
    return flask.render_template("signup.html", errors=enumerate(errors))


def signin_action():
    errors = validate_credentials()

    if len(errors):
        for error in errors:
            flask.flash(error, category="error")
        return flask.redirect(flask.url_for("signin_page"))

    username = flask.request.form.get("username")
    plain_password = flask.request.form.get("password")

    user, error = auth_service.get_user(username)
    if error:
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("signin_page"))

    if not check_password_hash(user.password_hash, plain_password):
        flask.flash("Virheellinen käyttäjätunnus ja/tai salasana")
        return flask.redirect(flask.url_for("signin_page"))

    return flask.redirect(flask.url_for("index_page"))


def signup_action():
    errors = validate_credentials()

    if len(errors):
        for error in errors:
            flask.flash(error, category="error")
        return flask.redirect(flask.url_for("signup_page"))

    username = flask.request.form.get("username")
    password = flask.request.form.get("password")

    _, error = auth_service.create_user(username, password)

    if error:
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("signup_page"))

    return flask.redirect(flask.url_for("index_page"))


def validate_credentials():
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    client_csrf_token = flask.request.form.get("csrf_token")
    server_csrf_token = flask.session.get("csrf_token")

    errors = []

    if not username:
        errors.append("Käyttäjätunnus on pakollinen")

    if not password:
        errors.append("Salasana on pakollinen")

    if not client_csrf_token or not server_csrf_token:
        errors.append("CSRF token puuttuu")
        return errors

    if client_csrf_token != server_csrf_token:
        errors.append("CSRF tokenin validointi virhe")

    return errors
