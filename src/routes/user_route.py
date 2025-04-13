import math
import flask
from services import user_service
from services import note_service
from decorators.login_required import login_required
from util.error import flash_errors
from util.generate_pagination_buttons import generate_pagination_buttons


@login_required
def user_page(username: str):
    """Render a user page or an error page based on the provided username."""

    user, _ = user_service.get_user_by_username(username)

    if not user:
        return flask.render_template(
            "error.html",
            message="Käyttäjää ei valitettavasti löydetty",
            code="404",
        )

    page = flask.request.args.get("page", default="1")
    if not page.isnumeric():
        return flash_errors("Virheellinen sivunumero", "index_page", page="1")

    page = int(page)
    limit = 24
    offset = limit * (page - 1)

    notes = note_service.get_notes_by_user(user, limit, offset)
    statistics = user_service.get_user_statistics(user)

    page_count = math.ceil(statistics.note_count / limit)
    pagination = generate_pagination_buttons(page, page_count)

    return flask.render_template(
        "user.html",
        user=user,
        notes=notes,
        statistics=statistics,
        page=page,
        pagination=pagination,
    )
