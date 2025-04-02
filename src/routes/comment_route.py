import flask
from util.error import flash_errors
from services import comment_service
from decorators import csrf
from decorators.flash_fields import flash_fields
from decorators.login_required import login_required


@login_required
@csrf.validate()
@flash_fields
def create_comment_action(note_id: int):
    """
    Create a new comment for a note.

    Args:
        note_id (int): The identifier of the note to which the comment is being added.

    Returns:
        A Flask redirect response to the note view page if the comment is created
        successfully, or a response with flashed error messages if validation fails.
    """
    content, user = _get_comment_details()
    error = _validate_comment(content)
    if error:
        return flash_errors(error, "view_note_page", note_id=note_id)

    comment_service.create_comment(content, user.id, note_id)

    return flask.redirect(flask.url_for("view_note_page", note_id=note_id))


def _get_comment_details():
    content = flask.request.form.get("content")
    user = flask.request.user
    return content, user


def _validate_comment(comment: str):
    if not comment or len(comment) < 3:
        return "Kommentti on liian lyhyt"
    if len(comment) > 1_000:
        return "Kommentti on liian pitkä"
    return None
