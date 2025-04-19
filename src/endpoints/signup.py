from flask import request, render_template, session
from typing import Optional, Self


class Signup(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(Signup, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        username: str = session["username"]
        error: str = ""
        
        if "error" in session.keys():
            error = session.pop("error")
        return render_template("signup.html", username=username, error=error)
