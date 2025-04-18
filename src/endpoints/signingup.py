from bcrypt import gensalt, hashpw
from data_instance import DataInstance
from flask import request, redirect, session, url_for
from typing import Optional, Self


class SigningUp(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(SigningUp, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        if request.method == "GET": return redirect(url_for("signup"))

        username = request.form["username"]
        username_taken: bool = username.lower() in DataInstance().db().keys()
        if not username_taken:
            DataInstance().db()[username.lower()] = {
                "username": username,
                "password": hashpw(request.form["password"].encode(), gensalt()).decode(),
                "preferred_choice": request.form["preferred_choice"],
                "total_wins": 0,
                "total_loses": 0,
                "total_draws": 0,
                "queue": [],
                "games": []
            }
            DataInstance().commit_db()
        
        if username_taken:
            session["error"] = "Username Taken"
            return redirect(url_for("signup"))
        session["username"] = username
        return redirect(url_for("login"))
