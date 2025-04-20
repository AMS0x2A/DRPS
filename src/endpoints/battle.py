from flask import render_template, session
from typing import Optional, Self


class Battle(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(Battle, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        username: str = session["username"]
        outcome: str = ""
        error: str = ""

        if "outcome" in session.keys():
            outcome = session.pop("outcome")

        if "error" in session.keys():
            error = session.pop("error")

        return render_template("battle.html", username=username, outcome=outcome, error=error)
