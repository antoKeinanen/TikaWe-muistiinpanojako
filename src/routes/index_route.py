import flask
from decorators.login_required import login_required
from services import note_service


@login_required
def index_page():
    """
    Render the index page with recent notes.

    This function retrieves recent notes using the `note_service` and renders
    the "index.html" template with these notes.

    Returns:
        Response: A Flask response object that renders the "index.html" template
        with the recent notes.
    """

    notes = note_service.get_recent_notes()
    return flask.render_template("index.html", notes=notes)
