import flask
from decorators.login_required import login_required
from services import note_service


@login_required
def search_page():
    """Render the search page with notes' title matching the query."""

    query = flask.request.args.get("query", "")

    notes = note_service.get_note_by_query(query)
    return flask.render_template("search.html", notes=notes, query=query)
