import flask
import math
from decorators.login_required import login_required
from services import note_service
from util.error import flash_errors
from util.generate_pagination_buttons import generate_pagination_buttons


@login_required
def index_page():
    """Render the index page with recent notes."""
    page = flask.request.args.get("page", default="1")
    if not page.isnumeric():
        return flash_errors("Virheellinen sivunumero", "index_page", page="1")

    page = int(page)
    limit = 40
    offset = limit * (page - 1)
    notes, note_count = note_service.get_recent_notes(limit, offset)
    page_count = math.ceil(note_count / limit)
    pagination = generate_pagination_buttons(page, page_count)

    return flask.render_template(
        "index.html",
        notes=notes,
        page=page,
        pagination=pagination,
    )
