import flask
from decorators.login_required import login_required
from services import note_service


@login_required
def index_page():
    notes = note_service.get_recent_notes()
    return flask.render_template("index.html", notes=notes)
