from endpoints.index import Index
from endpoints.signup import Signup
from endpoints.signingup import SigningUp
from endpoints.login import Login
from endpoints.loggingin import LoggingIn
from endpoints.logout import Logout
from endpoints.battle import Battle
from endpoints.battling import Battling
from endpoints.history import History

from data_instance import DataInstance
from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app() -> Flask:
    _app: Flask = Flask(
        __name__,
        static_folder=DataInstance().static_dir_path(),
        template_folder=DataInstance().templates_dir_path()
    )
    _app.secret_key = b'c00edd0f6c62a70d432eed87a0318c2dc905668a6902a0b4f3e6dcc281f8dd07'

    @_app.route("/status", methods=["GET"])
    def status(): return jsonify({"status": "healthy"})

    @_app.route("/", methods=["GET"])
    def index(): return Index().endpoint()
    
    @_app.route("/signup", methods=["GET"])
    def signup(): return Signup().endpoint()
    
    @_app.route("/signingup", methods=["GET", "POST"])
    def signingup(): return SigningUp().endpoint()
    
    @_app.route("/login", methods=["GET"])
    def login(): return Login().endpoint()
    
    @_app.route("/loggingin", methods=["GET", "POST"])
    def loggingin(): return LoggingIn().endpoint()
    
    @_app.route("/logout", methods=["GET"])
    def logout(): return Logout().endpoint()
    
    @_app.route("/battle", methods=["GET"])
    def battle(): return Battle().endpoint()
    
    @_app.route("/battling", methods=["GET", "POST"])
    def battling(): return Battling().endpoint()
    
    @_app.route("/history", methods=["GET"])
    def history(): return History().endpoint()

    _app.wsgi_app = ProxyFix(_app.wsgi_app)
    return _app
