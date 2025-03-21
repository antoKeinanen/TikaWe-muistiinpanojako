from flask import Flask
import routes.auth_route
import routes.index_route
import routes.note_route
from util.config import parse_config

app = Flask(__name__)

config = parse_config()
app.secret_key = config["CSRF_SECRET"]

app.add_url_rule("/", view_func=routes.index_route.index_page)
app.add_url_rule("/signup", view_func=routes.auth_route.signup_page)
app.add_url_rule("/signin", view_func=routes.auth_route.signin_page)
app.add_url_rule("/signout", view_func=routes.auth_route.signout_action)
app.add_url_rule("/note/create", view_func=routes.note_route.create_note_page)
app.add_url_rule("/note/<int:note_id>", view_func=routes.note_route.view_note_page)

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
