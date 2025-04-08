import flask
from decorators import csrf
from models.user import User
from models.note import Note
from services import note_service, comment_service
from util.error import flash_errors
from decorators.flash_fields import flash_fields
from decorators.login_required import login_required


@login_required
@csrf.setup
def create_note_page():  # noqa: D103
    return flask.render_template("notes/create_note.html")


@login_required
@csrf.setup
def edit_note_page(note_id: int):
    """Render the edit note page for a given note ID."""

    note, error = note_service.get_note_by_id(note_id)
    if error:
        return flash_errors(error, "view_note_page", note_id=note_id)

    user = flask.request.user

    if not _check_is_creator(note, user):
        error = "Sinulla ei ole oikeutta muokata tätä muistiinpanoa"
        return flash_errors(error, "view_note_page", note_id=note_id)

    return flask.render_template("notes/edit_note.html", note=note)


@login_required
@csrf.setup
def view_note_page(note_id: int):
    """Handle the request to view a specific note."""

    note, error = note_service.get_note_by_id(note_id)
    if error:
        return flash_errors(error, "index_page")

    comments = comment_service.get_note_comments(note_id)
    user: User = flask.request.user

    return flask.render_template(
        "notes/view_note.html",
        note=note,
        is_creator=user.id == note.user_id,
        comments=comments,
    )


@login_required
@csrf.validate("index_page")
def delete_note_action(note_id: int):
    """Handle the action to delete a specific note."""

    note, error = note_service.get_note_by_id(note_id)
    if error:
        return flash_errors(error, "view_note_page", note_id=note_id)

    user = flask.request.user

    if not _check_is_creator(note, user):
        error = "Sinulla ei ole oikeutta poistaa tätä muistiinpanoa"
        return flash_errors(error, "view_note_page", note_id=note_id)

    note_service.delete_note_by_id(note_id)

    return flask.redirect(flask.url_for("index_page"))


@login_required
@csrf.validate("index_page")
@flash_fields
def update_note_action(note_id: int):
    """Handle the action to update a specific note."""

    title, content = _get_form_data()
    errors = _validate_note(title, content)
    if errors:
        return flash_errors(errors, "create_note_page")

    user: User = flask.request.user
    note, error = note_service.get_note_by_id(note_id)
    if error:
        return flash_errors(error, "view_note_page", note_id=note_id)

    if not _check_is_creator(note, user):
        error = "Sinulla ei ole oikeutta muokata tätä muistiinpanoa"
        return flash_errors(error, "view_note_page", note_id=note_id)

    note_service.update_note_by_id(note_id, title, content)

    return flask.redirect(flask.url_for("view_note_page", note_id=note_id))


@login_required
@csrf.validate("index_page")
@flash_fields
def create_note_action():
    """Handle the action to create a new note."""

    title, content = _get_form_data()
    errors = _validate_note(title, content)
    if errors:
        return flash_errors(errors, "create_note_page")

    user: User = flask.request.user
    new_note_id = note_service.create_note(title, content, user.id)

    next_url = flask.url_for("view_note_page", note_id=new_note_id)
    return flask.redirect(next_url)


def _check_is_creator(note: Note, user: User):
    """
    Check if the given user is the creator of the given note.

    Args:
        note (Note): The note to be checked.
        user (User): The user to be checked against the note.

    Returns:
        bool: True if the user is the creator of the note, False otherwise.
    """

    return note.user_id == user.id


def _get_form_data():
    """
    Retrieve form data for title, and content.

    Returns:
        tuple: A tuple containing the title, and content.
    """

    title = flask.request.form.get("title")
    content = flask.request.form.get("content")

    return title, content


def _validate_note(title: str, content: str):
    """
    Validate the title and content of a note.

    Args:
        title (str): The title of the note to be validated.
        content (str): The content of the note to be validated.

    Returns:
        list: A list of error messages indicating any validation failures.
        If there are no errors, the list will be empty.
    """

    errors = []

    if not title:
        errors.append("Muistiinpanolle on annettava otsikko")
    elif len(title) > 64:
        errors.append("Otsikko on liian pitkä")
    elif len(title) < 3:
        errors.append("Otsikko on liian lyhyt")

    if not content:
        errors.append("Muistiinpanossa on oltava tekstiä")
    elif len(content) > 10_000:
        errors.append("Muistiinpanon on oltava alle 10 000 merkkiä pitkä")

    return errors
