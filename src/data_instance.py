from bcrypt import checkpw
from bson import ObjectId
from dotenv import dotenv_values
from pathlib import Path
from pymongo.collection import Collection
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi, ServerApiVersion
from typing import Literal, Optional, OrderedDict, Self


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

    __port: int = 14642

    __CONFIG: OrderedDict = dotenv_values()
    __host: str = __CONFIG["HOST"]
    __APP_SECRET_KEY: bytes = __CONFIG["SECRET_KEY"].encode()
    __MONGO_CLIENT = MongoClient(
        __CONFIG["MONGO_URI"],
        server_api=ServerApi(ServerApiVersion.V1)
    )
    __USERNAMES_ID = __CONFIG["USERNAMES_ID"]

    __DB: Optional[Collection] = None
    try:
        __DB = __MONGO_CLIENT.get_database(
            __CONFIG["DATABASE_NAME"]
        ).get_collection("Accounts")
    except Exception as e:
        raise Exception("Cannot initialize MongoDB", e)
    
    del __CONFIG

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

    def db(cls) -> Collection: return cls.__DB

    def create_user(cls, username: str, hashed_password: str, preferred_choice: Literal["rock", "paper", "scissors"]) -> bool:
        if cls.user_exists(username): return False
        
        cls.db().insert_one({
            "username": username,
            "password": hashed_password,
            "preferred_choice": preferred_choice,
            "total_wins": 0,
            "total_loses": 0,
            "total_draws": 0,
            "queue": [],
            "games": []
        })

        usernames = cls.db().find_one({"_id": ObjectId(cls.__USERNAMES_ID)})
        usernames["usernames"].append(username.lower())
        cls.db().update_one({"_id": ObjectId(cls.__USERNAMES_ID)}, {"$set": usernames})
        return True
    
    def user_exists(cls, username: str) -> bool:
        return username.lower() in cls.db().find_one({"_id": ObjectId(cls.__USERNAMES_ID)})["usernames"]
    
    def user_lost(cls, username: str, user_choice: Literal["rock", "paper", "scissors"], 
                  opp_username: str, opp_choice: Literal["rock", "paper", "scissors"]):
        user = cls.db().find_one({"username": username})
        if not user: return
        user["total_loses"] += 1
        cls.db().update_one({"_id": user["_id"]}, {"$set": user})
        cls.__user_played(username, user_choice, opp_username, opp_choice, -1)
    
    def user_won(cls, username: str, user_choice: Literal["rock", "paper", "scissors"], 
                  opp_username: str, opp_choice: Literal["rock", "paper", "scissors"]):
        user = cls.db().find_one({"username": username})
        if not user: return
        user["total_wins"] += 1
        cls.db().update_one({"_id": user["_id"]}, {"$set": user})
        cls.__user_played(username, user_choice, opp_username, opp_choice, 1)
    
    def user_drew(cls, username: str, user_choice: Literal["rock", "paper", "scissors"], 
                  opp_username: str, opp_choice: Literal["rock", "paper", "scissors"]):
        user = cls.db().find_one({"username": username})
        if not user: return
        user["total_draws"] += 1
        cls.db().update_one({"_id": user["_id"]}, {"$set": user})
        cls.__user_played(username, user_choice, opp_username, opp_choice, 0)
    
    def __user_played(cls, username: str, user_choice: Literal["rock", "paper", "scissors"], 
                  opp_username: str, opp_choice: Literal["rock", "paper", "scissors"],
                  outcome: Literal[-1, 0, 1]):
        user = cls.db().find_one({"username": username})
        if not user: return
        user["games"].insert(
            0, {
                "choice": user_choice,
                "opponent": opp_username,
                "opp_choice": opp_choice,
                "result": "W" if outcome == 1 else "L" if outcome == -1 else "D"
            }
        )
        result = cls.db().update_one({"_id": user["_id"]}, {"$set": user})
        print(result.modified_count)

    def check_password(cls, username: str, password: str) -> bool:
        user = cls.db().find_one({"username": username})
        if not user: return False
        return checkpw(
            password.encode(), 
            user["password"].encode()
        )
    
    def get_user(cls, username: str):
        return cls.db().find_one({"username": username})

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
