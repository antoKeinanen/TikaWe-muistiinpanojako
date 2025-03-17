from flask import Flask
import routes
import routes.auth
import routes.index
from util.config import parse_config

app = Flask(__name__)

config = parse_config()
app.secret_key = config["CSRF_SECRET"]

app.add_url_rule("/", view_func=routes.index.index_page)
app.add_url_rule("/signup", view_func=routes.auth.signup_page)
app.add_url_rule("/signin", view_func=routes.auth.signin_page)
