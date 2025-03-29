import flask
from decorators.login_required import login_required
from services import note_service


@login_required
def search_page():
    """
    Render the search page with notes' title matching the query.

    Retrieves the query from the request's arguments, searches for
    notes matching the query using the note_service, and renders
    the search.html template with the found notes.

    Returns:
        Response: Rendered search.html template.
    """

    query = flask.request.args.get("query", "")

    notes = note_service.get_note_by_query(query)
    return flask.render_template("search.html", notes=notes, query=query)
