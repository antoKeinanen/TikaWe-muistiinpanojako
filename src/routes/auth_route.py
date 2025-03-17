import secrets
import flask
from services import auth_service


def signin_page():
    flask.session["csrf_token"] = secrets.token_hex(16)
    return flask.render_template("signin.html")


def signup_page():
    errors = flask.get_flashed_messages(category_filter="error")
    flask.session["csrf_token"] = secrets.token_hex(16)
    return flask.render_template("signup.html", errors=enumerate(errors))


def signup_action():
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    client_csrf_token = flask.request.form.get("csrf_token")
    server_csrf_token = flask.session.get("csrf_token")

    invalid = False

    if not username:
        flask.flash("Käyttäjätunnus on pakollinen", category="error")
        invalid = True

    if not password:
        flask.flash("Salasana on pakollinen", category="error")
        invalid = True

    if invalid:
        return flask.redirect(flask.url_for("signup_page"))

    if not client_csrf_token or not server_csrf_token:
        flask.flash("Puuttuva CSRF token", category="error")
        return flask.redirect(flask.url_for("signup_page"))

    if client_csrf_token != server_csrf_token:
        flask.flash("CSRF tokenin validointi virhe", category="error")
        return flask.redirect(flask.url_for("signup_page"))

    creation_error = auth_service.create_user(username, password)

    if creation_error:
        flask.flash(creation_error, category="error")
        return flask.redirect(flask.url_for("signup_page"))

    return flask.redirect(flask.url_for("index_page"))
