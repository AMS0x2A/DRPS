from flask import redirect, session, url_for
from typing import Optional, Self


class Logout(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(Logout, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        session.clear()
        return redirect(url_for("index"))
