from flask import render_template, session
from typing import Optional, Self


class Index(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(Index, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        username: str = session["username"]
        return render_template("index.html", username=username)
