from flask import Flask
import routes.auth_route
import routes.index_route
import routes.note_route
import routes.search_route
import routes.comment_route
import routes.user_route
from util.config import config
from injectors.error_injector import inject_errors
from injectors.field_injector import inject_fields

app = Flask(__name__, static_folder="static")
app.secret_key = config.csrf_secret

app.context_processor(inject_errors)
app.context_processor(inject_fields)

app.add_url_rule("/", view_func=routes.index_route.index_page)
app.add_url_rule("/signup", view_func=routes.auth_route.signup_page)
app.add_url_rule("/signin", view_func=routes.auth_route.signin_page)
app.add_url_rule("/search", view_func=routes.search_route.search_page)
app.add_url_rule("/signout", view_func=routes.auth_route.signout_action)
app.add_url_rule("/note/create", view_func=routes.note_route.create_note_page)
app.add_url_rule("/note/<int:note_id>", view_func=routes.note_route.view_note_page)
app.add_url_rule("/note/<int:note_id>/edit", view_func=routes.note_route.edit_note_page)
app.add_url_rule("/user/<string:username>", view_func=routes.user_route.user_page)

app.add_url_rule(
    "/api/signup",
    view_func=routes.auth_route.signup_action,
    methods=["POST"],
)
app.add_url_rule(
    "/api/signin",
    view_func=routes.auth_route.signin_action,
    methods=["POST"],
)
app.add_url_rule(
    "/api/note/new",
    view_func=routes.note_route.create_note_action,
    methods=["POST"],
)
app.add_url_rule(
    "/api/note/<int:note_id>/update",
    view_func=routes.note_route.update_note_action,
    methods=["POST"],
)
app.add_url_rule(
    "/api/note/<int:note_id>/delete",
    view_func=routes.note_route.delete_note_action,
    methods=["POST"],
)
app.add_url_rule(
    "/api/comment/<int:note_id>/new",
    view_func=routes.comment_route.create_comment_action,
    methods=["POST"],
)
