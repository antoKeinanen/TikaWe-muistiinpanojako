import secrets
from flask import render_template, session


def signin_page():
    session["csrf_token"] = secrets.token_hex(16)
    return render_template("signin.html")


def signup_page():
    session["csrf_token"] = secrets.token_hex(16)
    return render_template("signup.html")
