from data_instance import DataInstance
from flask import request, redirect, session, url_for
from typing import Optional, Self


class LoggingIn(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(LoggingIn, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        if request.method == "GET": return redirect(url_for("login"))
        username: str = request.form["username"]
        password: str = request.form["password"]

        if not DataInstance().user_exists(username) or not DataInstance().check_password(username, password):
            session["error"] = "Username/Password Incorrect"
            return redirect(url_for("login"))
        
        session["username"] = username
        return redirect(url_for("index"))
