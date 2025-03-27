import flask
from decorators import csrf
from decorators.login_required import login_required
from services import note_service
from util.logger import Logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User


@login_required
@csrf.setup
def create_note_page():
    errors = flask.get_flashed_messages(category_filter="error")
    return flask.render_template(
        "notes/create_note.html",
        errors=enumerate(errors),
        error_count=len(errors),
    )


@login_required
@csrf.setup
def edit_note_page(note_id: int):
    errors = flask.get_flashed_messages(category_filter="error")
    note, error = note_service.get_note_by_id(note_id, join_user=True)
    if error:
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("view_note_page", note_id=note_id))

    user = flask.request.user

    if note.user_id != user.id:
        Logger.error("Unauthorized note access")
        flask.flash(
            "Sinulla ei ole oikeutta muokata tätä muistiinpanoa",
            category="error",
        )
        return flask.redirect(flask.url_for("view_note_page", note_id=note_id))

    return flask.render_template(
        "notes/edit_note.html",
        note=note,
        errors=enumerate(errors),
        error_count=len(errors),
    )


@login_required
@csrf.setup
def view_note_page(note_id: int):
    note, error = note_service.get_note_by_id(note_id, join_user=True)
    if error:
        Logger.error(error)
        return flask.redirect(flask.url_for("index_page"))

    user: User = flask.request.user
    Logger.log(user, note, user.id == note.user_id)

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
        Logger.error(error)
        return flask.redirect(flask.url_for("view_note_page", note_id=note_id))

    user = flask.request.user

    if note.user_id != user.id:
        return flask.redirect(flask.url_for("view_note_page", note_id=note_id))

    _, error = note_service.delete_note_by_id(note_id)
    if error:
        Logger.error(error)
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("view_note_page", note_id=note_id))

    return flask.redirect(flask.url_for("view_note_page", note_id=note_id))


@login_required
@csrf.validate("index_page")
def update_note_action(note_id: int):
    errors = validate_note()

    if len(errors):
        for error in errors:
            flask.flash(error, category="error")
        return flask.redirect(flask.url_for("create_note_page"))

    title = flask.request.form.get("title")
    content = flask.request.form.get("content")
    user: User = flask.request.user

    note, error = note_service.get_note_by_id(note_id)
    if error:
        Logger.error(error)
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("view_note_page", note_id=note_id))

    if note.user_id != user.id:
        Logger.error("Unauthorized note access")
        flask.flash(
            "Sinulla ei ole oikeutta muokata tätä muistiinpanoa",
            category="error",
        )
        return flask.redirect(flask.url_for("view_note_page", note_id=note_id))

    _, error = note_service.update_note_by_id(note_id, title, content)
    if error:
        Logger.error(error)
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("view_note_page", note_id=note_id))

    return flask.redirect(flask.url_for("view_note_page", note_id=note_id))


@login_required
@csrf.validate("index_page")
def create_note_action():
    errors = validate_note()

    if len(errors):
        for error in errors:
            flask.flash(error, category="error")
        return flask.redirect(flask.url_for("create_note_page"))

    title = flask.request.form.get("title")
    content = flask.request.form.get("content")

    user: User = flask.request.user

    new_note, error = note_service.create_note(title, content, user.id)

    if error:
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("create_note_page"))

    next_url = flask.url_for("view_note_page", note_id=new_note.id)
    return flask.redirect(next_url)


def validate_note():
    title = flask.request.form.get("title")
    content = flask.request.form.get("content")

    errors = []

    if not title:
        errors.append("Muistiinpanolle on annettava otsikko")
    elif len(title) > 24:
        errors.append("Otsikko on liian pitkä")
    elif len(title) < 3:
        errors.append("Otsikko on liian lyhyt")

    if not content:
        errors.append("Muistiinpanossa on oltava tekstiä")
    elif len(content) > 10_000:
        errors.append("Muistiinpanon on oltava alle 10 000 merkkiä pitkä")

    return errors
