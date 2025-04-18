from data_instance import DataInstance
from flask import redirect, render_template, session, url_for
from typing import Optional, Self


class History(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(History, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        username: str = ""
        if not "username" in session.keys(): return redirect(url_for("login"))
        username = session["username"]
        queue = DataInstance().db()[username.lower()]["queue"]
        history = DataInstance().db()[username.lower()]["games"]
        return render_template("history.html", username=username, queue=queue, games=history)
