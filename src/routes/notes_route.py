import flask
from decorators import csrf
from decorators.login_required import login_required
from models.user import User


@login_required
@csrf.setup
def create_note_page(_user: User):
    errors = flask.get_flashed_messages(category_filter="error")
    return flask.render_template("notes/create_note.html", errors=enumerate(errors))
