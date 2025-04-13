import math
import flask
from decorators.login_required import login_required
from services import note_service
from util.error import flash_errors
from util.generate_pagination_buttons import generate_pagination_buttons


@login_required
def search_page():
    """Render the search page with notes' title matching the query."""

    query = flask.request.args.get("query", "")

    page = flask.request.args.get("page", default="1")
    if not page.isnumeric():
        return flash_errors("Virheellinen sivunumero", "search_page", page="1")

    page = int(page)
    limit = 40
    offset = limit * (page - 1)
    notes, note_count = note_service.get_note_by_query(query, limit, offset)
    page_count = math.ceil(note_count / limit)
    pagination = generate_pagination_buttons(page, page_count)

    return flask.render_template(
        "search.html",
        notes=notes,
        query=query,
        pagination=pagination,
        page=page,
    )
