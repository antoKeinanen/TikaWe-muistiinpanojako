import re
import flask
from decorators import csrf
from services import auth_service
from util.error import flash_errors
from decorators.flash_fields import flash_fields
from werkzeug.security import check_password_hash


@csrf.setup
def signin_page():
    """
    Handle the sign-in page rendering and redirection.

    If the user is already signed in (as determined by the session),
    they are redirected to the next page. Otherwise, the sign-in template
    is rendered.

    Returns:
        Response: A Flask response object that either redirects to the
        next page or renders the sign-in template.
    """

    if flask.session.get("signed_in"):
        next_page = _get_next_page()
        return flask.redirect(next_page)

    return flask.render_template("auth/signin.html")


@csrf.setup
def signup_page():
    """
    Handle the sign-up page rendering and redirection.

    If the user is already signed in (as determined by the session),
    they are redirected to the next page. Otherwise, the sign-up template
    is rendered.

    Returns:
        Response: A Flask response object that either redirects to the
        next page or renders the sign-up template.
    """

    if flask.session.get("signed_in"):
        next_page = _get_next_page()
        return flask.redirect(next_page)

    return flask.render_template("auth/signup.html")


@csrf.validate("signin_page")
@flash_fields
def signin_action():
    """
    Handle the sign-in action, validating user credentials and responding
    accordingly.

    Retrieves form data, validates the credentials, and
    checks the password against the stored hash. If there are any errors
    during this process, appropriate error messages are flashed and the
    user is redirected back to the sign-in page. On successful validation,
    a token is generated and the user is redirected to the next page.

    Returns:
        Response: A Flask response object that either flashes errors and
        redirects to the sign-in page or responds with a token and
        redirects to the next page.
    """

    username, plain_password, next_page = _get_form_data()
    errors = _validate_credentials(username, plain_password)
    if errors:
        return flash_errors(errors, "signin_page", next=next_page)

    user, error = auth_service.get_user_by_username(username)
    if error:
        return flash_errors(error, "signin_page", next=next_page)

    if not check_password_hash(user.password_hash, plain_password):
        error = "Virheellinen käyttäjätunnus ja/tai salasana"
        return flash_errors(error, "signin_page", next=next_page)

    return _respond_with_token(user.token, next_page)


@csrf.validate("signup_page")
@flash_fields
def signup_action():
    """
    Handle the sign-up action, validating user credentials and responding
    accordingly.

    Retrieves form data, validates the credentials for sign-up, and attempts to create
    a new user. If there are any errors during this process, appropriate error messages
    are flashed and the user is redirected back to the sign-up page. On successful user
    creation, a token is generated and the user is redirected to the next page.

    Returns:
        Response: A Flask response object that either flashes errors and
        redirects to the sign-up page or responds with a token and
        redirects to the next page.
    """

    username, plain_password, next_page = _get_form_data()
    errors = _validate_credentials_signup(username, plain_password)
    if errors:
        return flash_errors(errors, "signup_page", next=next_page)

    user, error = auth_service.create_user(username, plain_password)
    if error:
        return flash_errors(error, "signup_page", next=next_page)

    return _respond_with_token(user.token, next_page)


def signout_action():
    """
    Handle the sign-out action, clearing session and cookie data.

    Sets the session's "signed_in" flag to False, clears the
    "Authorization" cookie, and redirects the user to the sign-in page.

    Returns:
        Response: A Flask response object that redirects to the sign-in page
        and clears the "Authorization" cookie.

    """

    flask.session["signed_in"] = False
    response = flask.make_response(
        flask.redirect(flask.url_for("signin_page")),
    )
    response.set_cookie("Authorization", "")
    return response


def _validate_credentials_signup(username: str | None, password: str | None):
    """
    Validate the credentials provided during the sign-up process.

    Performs additional checks specific to the sign-up
    process, such as username length and password complexity. Builds
    upon the base credential validation by adding further constraints.

    Args:
        username (str | None): The username to validate.
        password (str | None): The password to validate.

    Returns:
        list: A list of error messages if validation fails, otherwise an
        empty list.
    """

    errors = _validate_credentials(username, password)

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
        and re.compile(r"[a-zåäö]").search(password)
    ):
        errors.append("Salasanassa on oltava isoja ja pieniä kirjaimia")

    return errors


def _validate_credentials(username: str | None, password: str | None):
    """
    Perform basic validation of credentials.

    Checks if the username and password are provided. Returns a list of error messages
    if either field is missing.

    Args:
        username (str | None): The username to validate.
        password (str | None): The password to validate.

    Returns:
        list: A list of error messages if validation fails, otherwise an
        empty list.
    """

    errors = []

    if not username:
        errors.append("Käyttäjätunnus on pakollinen")

    if not password:
        errors.append("Salasana on pakollinen")

    return errors


def _get_next_page():
    """
    Retrieve the next page URL from the form data or default to the index page.

    This function attempts to get the "next" page URL from the form data.
    If the "next" key is not present, it defaults to the URL for the index page.

    Returns:
        str: The URL for the next page or the index page if "next" is not
        specified in the form data.
    """

    return flask.request.form.get("next") or flask.url_for("index_page")


def _get_form_data():
    """
    Retrieve form data for username, password, and next page.

    This function extracts the username and password from the form data
    submitted via a POST request. It also retrieves the next page URL using
    the `_get_next_page` function.

    Returns:
        tuple: A tuple containing the username, password, and next page URL.
    """

    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    next_page = _get_next_page()
    return username, password, next_page


def _respond_with_token(token: str, redirect_to: str):
    """
    Create a response that sets an authorization token cookie and redirects to
    a specified URL.

    This function generates a Flask response that includes setting the "Authorization"
    cookie with the provided token. The response redirects the user to the given URL.

    Args:
        token (str): The authorization token to be set in the cookie.
        redirect_to (str): The URL to redirect the user to.

    Returns:
        Response: A Flask response object that sets the "Authorization" cookie and
        redirects to the specified URL.

    """
    response = flask.make_response(flask.redirect(redirect_to))
    response.set_cookie("Authorization", token, httponly=True, samesite="Strict")
    return response
