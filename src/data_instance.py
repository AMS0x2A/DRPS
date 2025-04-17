import json
from pathlib import Path
from typing import Dict, Optional, Self

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

    __host: str = "192.168.68.103"
    __port: int = 5000

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(DataInstance, cls).__new__(cls)
        return cls._instance
    
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
