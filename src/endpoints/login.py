from flask import render_template, session
from typing import Optional, Self


class Login(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(Login, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        username: str = ""
        error: str = ""
        if "username" in session.keys():
            username = session["username"]
        if "error" in session.keys():
            error = session.pop("error")
        return render_template("login.html", username=username, error=error)
