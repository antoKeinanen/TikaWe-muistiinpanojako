from flask import render_template
from decorators.login_required import login_required


@login_required
def index_page():
    return render_template("index.html")
