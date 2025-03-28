import flask
from decorators import csrf
from models.user import User
from models.note import Note
from services import note_service
from util.error import flash_errors
from decorators.flash_fields import flash_fields
from decorators.login_required import login_required


@login_required
@csrf.setup
def create_note_page():
    return flask.render_template("notes/create_note.html")


@login_required
@csrf.setup
def edit_note_page(note_id: int):
    note, error = note_service.get_note_by_id(note_id)
    if error:
        return flash_errors(error, "view_note_page", note_id=note_id)

    user = flask.request.user

    if _check_is_creator(note, user):
        error = "Sinulla ei ole oikeutta muokata tätä muistiinpanoa"
        return flash_errors(error, "view_note_page", note_id=note_id)

    return flask.render_template("notes/edit_note.html", note=note)


@login_required
@csrf.setup
def view_note_page(note_id: int):
    note, error = note_service.get_note_by_id(note_id)
    if error:
        return flash_errors(error, "index_page")

    user: User = flask.request.user

    return flask.render_template(
        "notes/view_note.html",
        note=note,
        is_creator=user.id == note.user_id,
    )


@login_required
@csrf.validate("index_page")
def delete_note_action(note_id: int):
    note, error = note_service.get_note_by_id(note_id)
    if error:
        return flash_errors(error, "view_note_page", note_id=note_id)

    user = flask.request.user

    if _check_is_creator(note, user):
        error = "Sinulla ei ole oikeutta muokata tätä muistiinpanoa"
        return flash_errors(error, "view_note_page", note_id=note_id)

    note_service.delete_note_by_id(note_id)

    return flask.redirect(flask.url_for("view_note_page", note_id=note_id))


@login_required
@csrf.validate("index_page")
@flash_fields
def update_note_action(note_id: int):
    title, content = _get_form_data()
    errors = _validate_note()
    if errors:
        return flash_errors(errors, "create_note_page")

    user: User = flask.request.user
    note, error = note_service.get_note_by_id(note_id)
    if error:
        return flash_errors("view_note_page", note_id=note_id)

    if _check_is_creator(note, user):
        error = "Sinulla ei ole oikeutta muokata tätä muistiinpanoa"
        return flash_errors(error, "view_note_page", note_id=note_id)

    note_service.update_note_by_id(note_id, title, content)

    return flask.redirect(flask.url_for("view_note_page", note_id=note_id))


@login_required
@csrf.validate("index_page")
@flash_fields
def create_note_action():
    title, content = _get_form_data()
    errors = _validate_note(title, content)
    if errors:
        return flash_errors(errors, "create_note_page")

    user: User = flask.request.user
    new_note_id = note_service.create_note(title, content, user.id)

    next_url = flask.url_for("view_note_page", note_id=new_note_id)
    return flask.redirect(next_url)


def _check_is_creator(note: Note, user: User):
    return note.id == user.id


def _get_form_data():
    title = flask.request.form.get("title")
    content = flask.request.form.get("content")

    return title, content


def _validate_note(title: str, content: str):
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
