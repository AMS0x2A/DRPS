import json
from bcrypt import checkpw
from pathlib import Path
from secrets import token_hex
from typing import Dict, Literal, Optional, Self

class DataInstance(object):
    _instance: Optional[Self] = None

    __SRC_DIR_PATH: Path = Path(__file__).parent
    __PROJECT_DIR_PATH: Path = __SRC_DIR_PATH.parent
    __RESOURCES_DIR_PATH: Path = Path(__PROJECT_DIR_PATH, "resources")
    __TEMPLATES_DIR_PATH: Path = Path(__RESOURCES_DIR_PATH, "templates")
    __STATIC_DIR_PATH: Path = Path(__RESOURCES_DIR_PATH, "static")
    __CSS_DIR_PATH: Path = Path(__STATIC_DIR_PATH, "css")
    __IMAGES_DIR_PATH: Path = Path(__STATIC_DIR_PATH, "images")
    __JSONS_DIR_PATH: Path = Path(__STATIC_DIR_PATH, "jsons")
    __DB_PATH: Path = Path(__JSONS_DIR_PATH, "db.json")

    __DB: Dict[str, Dict[str, str | int]] = json.load(open(__DB_PATH, "r"))

    __host: str = "localhost"
    __port: int = 5000

    __APP_SECRET_KEY: bytes = token_hex().encode()

    __SECRET_PY_PATH: Path = Path(__SRC_DIR_PATH, "secret.py")
    __SECRET_PY_PATH.touch()
    with open(__SECRET_PY_PATH, "w") as fh:
        fh.write(f"flask_secret = {__APP_SECRET_KEY}")

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(DataInstance, cls).__new__(cls)
        return cls._instance
    
    def app_secret_key(cls) -> bytes: return cls.__APP_SECRET_KEY
    def src_dir_path(cls) -> Path: return cls.__SRC_DIR_PATH
    def project_dir_path(cls) -> Path: return cls.__PROJECT_DIR_PATH
    def resources_dir_path(cls) -> Path: return cls.__RESOURCES_DIR_PATH
    def templates_dir_path(cls) -> Path: return cls.__TEMPLATES_DIR_PATH
    def static_dir_path(cls) -> Path: return cls.__STATIC_DIR_PATH
    def css_dir_path(cls) -> Path: return cls.__CSS_DIR_PATH
    def images_dir_path(cls) -> Path: return cls.__IMAGES_DIR_PATH
    def jsons_dir_path(cls) -> Path: return cls.__JSONS_DIR_PATH
    def db_path(cls) -> Path: return cls.__DB_PATH

    def db(cls) -> Dict[str, Dict[str, str | int]]: return cls.__DB
    def commit_db(cls):
        with open(cls.__DB_PATH, "w") as fh:
            json.dump(cls.__DB, fh, indent=4)

    def create_user(cls, username: str, hashed_password: str, preferred_choice: Literal["rock", "paper", "scissors"]) -> bool:
        if username.lower() in cls.db().keys(): return False
        cls.db()[username.lower()] = {
            "username": username,
            "password": hashed_password,
            "preferred_choice": preferred_choice,
            "total_wins": 0,
            "total_loses": 0,
            "total_draws": 0,
            "queue": [],
            "games": []
        } 
        cls.commit_db()
        return True
    
    def user_exists(cls, username: str) -> bool:
        return username.lower() in cls.db().keys()
    
    def user_lost(cls, username: str, user_choice: Literal["rock", "paper", "scissors"], 
                  opp_username: str, opp_choice: Literal["rock", "paper", "scissors"]):
        cls.db()[username.lower()]["total_loses"] += 1
        cls.__user_played(username, user_choice, opp_username, opp_choice, -1)
    
    def user_won(cls, username: str, user_choice: Literal["rock", "paper", "scissors"], 
                  opp_username: str, opp_choice: Literal["rock", "paper", "scissors"]):
        cls.db()[username.lower()]["total_wins"] += 1
        cls.__user_played(username, user_choice, opp_username, opp_choice, 1)
    
    def user_drew(cls, username: str, user_choice: Literal["rock", "paper", "scissors"], 
                  opp_username: str, opp_choice: Literal["rock", "paper", "scissors"]):
        cls.db()[username.lower()]["total_draws "] += 1
        cls.__user_played(username, user_choice, opp_username, opp_choice, 0)
    
    def __user_played(cls, username: str, user_choice: Literal["rock", "paper", "scissors"], 
                  opp_username: str, opp_choice: Literal["rock", "paper", "scissors"],
                  outcome: Literal[-1, 0, 1]):
        DataInstance().db()[username.lower()]["games"].insert(
            0, {
                "choice": user_choice,
                "opponent": opp_username,
                "opp_choice": opp_choice,
                "result": "W" if outcome == 1 else "L" if outcome == -1 else "D"
            }
        )
        DataInstance().commit_db()

    def check_password(cls, username: str, password: str) -> bool:
        return checkpw(
            password.encode(), 
            cls.db()[username.lower()]["password"].encode()
        )

    @property
    def host(cls) -> str:
        return cls.__host
    
    @host.setter
    def host(cls, value: str):
        cls.__host = value

    @property
    def port(cls) -> int:
        return cls.__port
    
    @port.setter
    def port(cls, value: int):
        cls.__port = value
