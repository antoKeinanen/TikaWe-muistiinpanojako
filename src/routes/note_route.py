import flask
from decorators import csrf
from decorators.login_required import login_required
from services import note_service
from pathlib import Path


@login_required
@csrf.setup
def create_note_page():
    errors = flask.get_flashed_messages(category_filter="error")
    return flask.render_template("notes/create_note.html", errors=enumerate(errors))


@login_required
@csrf.setup
def create_note_action():
    errors = validate_note()

    if len(errors):
        for error in errors:
            flask.flash(error, category="error")
        return flask.redirect(flask.url_for("create_note_page"))

    title = flask.request.form.get("title")
    content = flask.request.form.get("content")

    user = flask.session.user

    new_note, error = note_service.create_note(title, content, user.id)

    if error:
        flask.flash(error, category="error")
        return flask.redirect(flask.url_for("create_note_page"))

    next_url = Path(flask.url_for("create_note_page"), str(new_note.id))

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
