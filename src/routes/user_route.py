import flask
from services import user_service
from services import note_service
from decorators.login_required import login_required


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

    notes = note_service.get_notes_by_user(user)
    statistics = user_service.get_user_statistics(user)

    return flask.render_template(
        "user.html",
        user=user,
        notes=notes,
        statistics=statistics,
    )
