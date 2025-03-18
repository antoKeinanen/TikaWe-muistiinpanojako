from flask import render_template
from decorators.login_required import login_required
from models.user import User


@login_required
def index_page(_user: User):
    return render_template("index.html")
