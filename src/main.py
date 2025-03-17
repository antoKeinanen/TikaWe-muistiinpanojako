from flask import Flask
import routes
import routes.auth_route
import routes.index
from util.config import parse_config

app = Flask(__name__)

config = parse_config()
app.secret_key = config["CSRF_SECRET"]

app.add_url_rule("/", view_func=routes.index.index_page)
app.add_url_rule("/signup", view_func=routes.auth_route.signup_page)
app.add_url_rule("/signin", view_func=routes.auth_route.signin_page)

app.add_url_rule(
    "/api/signup",
    view_func=routes.auth_route.signup_action,
    methods=["POST"],
)
