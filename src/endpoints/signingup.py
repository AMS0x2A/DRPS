from bcrypt import gensalt, hashpw
from src.data_instance import DataInstance
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
        username_taken: bool = DataInstance().user_exists(username)

        if username_taken:
            session["error"] = "Username Taken"
            return redirect(url_for("signup"))
        
        if not username_taken:
            DataInstance().create_user(
                username, 
                hashpw(request.form["password"].encode(), gensalt()).decode(),
                request.form["preferred_choice"]
            )
        
        session["username"] = username
        return redirect(url_for("login"))
