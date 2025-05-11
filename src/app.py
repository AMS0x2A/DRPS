from src.endpoints.index import Index
from src.endpoints.signup import Signup
from src.endpoints.signingup import SigningUp
from src.endpoints.login import Login
from src.endpoints.loggingin import LoggingIn
from src.endpoints.logout import Logout
from src.endpoints.battle import Battle
from src.endpoints.battling import Battling
from src.endpoints.history import History

from src.data_instance import DataInstance
from src.endpoint_wrappers import login_required
from flask import Flask, jsonify, session
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app() -> Flask:
    _app: Flask = Flask(
        __name__,
        static_folder=DataInstance().static_dir_path(),
        template_folder=DataInstance().templates_dir_path()
    )
    _app.secret_key = DataInstance().app_secret_key()

    @_app.before_request
    def check_login():
        if "username" not in session.keys():
            session["username"] = ""

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
    @login_required
    def battle(): return Battle().endpoint()
    
    @_app.route("/battling", methods=["GET", "POST"])
    @login_required
    def battling(): return Battling().endpoint()
    
    @_app.route("/history", methods=["GET"])
    @login_required
    def history(): return History().endpoint()

    _app.wsgi_app = ProxyFix(_app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    return _app
