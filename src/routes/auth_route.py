import flask
from services import auth_service
from werkzeug.security import check_password_hash
import re
from decorators import csrf
from decorators.flash_fields import flash_fields


@csrf.setup
def signin_page():
    if flask.session.get("signed_in"):
        next_page = flask.request.form.get("next")

        if not next_page or not len(next_page):
            next_page = flask.url_for("index_page")
        return flask.redirect(next_page)

    return flask.render_template("auth/signin.html")


@csrf.setup
def signup_page():
    if flask.session.get("signed_in"):
        next_page = flask.request.form.get("next")

        if not next_page or not len(next_page):
            next_page = flask.url_for("index_page")
        return flask.redirect(next_page)

    return flask.render_template("auth/signup.html")


@csrf.validate("signin_page")
@flash_fields
def signin_action():
    username = flask.request.form.get("username")
    plain_password = flask.request.form.get("password")

    errors = validate_credentials(username, plain_password)
    if len(errors):
        for error in errors:
            flask.flash(error, category="error")
        return flask.redirect(flask.url_for("signin_page"))

    user, error = auth_service.get_user_by_username(username)
    if error:
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("signin_page"))

    if not check_password_hash(user.password_hash, plain_password):
        flask.flash("Virheellinen käyttäjätunnus ja/tai salasana", category="error")
        return flask.redirect(flask.url_for("signin_page"))

    next_page = flask.request.form.get("next")

    if not next_page or not len(next_page):
        next_page = flask.url_for("index_page")

    response = flask.make_response(flask.redirect(next_page))
    # Here you should also set secure to true if this was a real production application
    response.set_cookie("Authorization", user.token, httponly=True, samesite="Strict")
    return response


@csrf.validate("signup_page")
@flash_fields
def signup_action():
    username = flask.request.form.get("username")
    plain_password = flask.request.form.get("password")

    errors = validate_credentials_signup(username, plain_password)
    if len(errors):
        for error in errors:
            flask.flash(error, category="error")
        return flask.redirect(flask.url_for("signup_page"))

    user, error = auth_service.create_user(username, plain_password)

    if error:
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("signup_page"))

    next_page = flask.request.form.get("next")

    if not next_page or not len(next_page):
        next_page = flask.url_for("index_page")

    response = flask.make_response(flask.redirect(next_page))
    # Here you should also set secure to true if this was a real production application
    response.set_cookie("Authorization", user.token, httponly=True, samesite="Strict")
    return response


def signout_action():
    flask.session["signed_in"] = False
    response = flask.make_response(
        flask.redirect(flask.url_for("signin_page")),
    )
    response.set_cookie("Authorization", "")
    return response


def validate_credentials_signup(username: str | None, password: str | None):
    errors = validate_credentials(username, password)

    if errors:
        return errors

    if len(username) > 16:
        errors.append("Käyttäjätunnus on liian pitkä")
    elif len(username) < 3:
        errors.append("Käyttäjätunnus on liian lyhyt")

    if len(password) < 8:
        errors.append("Salasanassa on oltava vähintään 8 merkkiä")
    elif len(password) > 255:
        errors.append("Salasanan tulee olla alle 255 merkkiä pitkä")
    elif not (
        re.compile(r"[A-ZÅÄÖ]").search(password)
        or not re.compile(r"[a-zåäö]").search(password)
    ):
        errors.append("Salasanassa on oltava isoja ja pieniä kirjaimia")

    return errors


def validate_credentials(username: str | None, password: str | None):
    errors = []

    if not username:
        errors.append("Käyttäjätunnus on pakollinen")

    if not password:
        errors.append("Salasana on pakollinen")

    return errors
