from flask import session, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not "username" in session.keys() or session["username"] == "":
            session["username"] = ""
            session["error"] = "Login required"
            return redirect(url_for("login"))
        return f()
    return decorator
    