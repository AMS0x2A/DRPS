from bcrypt import checkpw
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
        if request.method == "GET": 
            return redirect(url_for("login"))
        username: str = request.form["username"]
        password: str = request.form["password"]

        session["username"] = username
        if (
            not username.lower() in DataInstance().db().keys()
        ) or (
            not checkpw(
                password.encode(), 
                DataInstance().db()[username.lower()]["password"].encode()
            )
        ):
            session["error"] = "Username/Password Incorrect"
            return redirect(url_for("login"))
        return redirect(url_for("index"))
