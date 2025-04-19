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
        username: str = session["username"]
        queue = DataInstance().get_user(username)["queue"]
        history = DataInstance().get_user(username)["games"]
        return render_template("history.html", username=username, queue=queue, games=history)
