from bcrypt import checkpw, gensalt, hashpw
from data_instance import DataInstance
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from random import choice
from typing import Dict, List
from werkzeug.middleware.proxy_fix import ProxyFix


def determine_winner(choice: str, other_choice: str) -> int:
    """
    1 if choice beats other_choice
    0 if draws
    -1 if other_choice beats choice
    """
    if choice == other_choice: return 0
    match (choice, other_choice):
        case ("rock", "paper"): return -1
        case ("rock", _): return 1
        case ("paper", _): return 1
        case ("paper", "scissors"): return -1
        case ("scissors", "rock"): return -1
        case ("scissors", _): return 1
    return 0 


def create_app() -> Flask:
    _app: Flask = Flask(
        __name__,
        static_folder=DataInstance().static_dir_path(),
        template_folder=DataInstance().templates_dir_path()
    )
    _app.secret_key = b'c00edd0f6c62a70d432eed87a0318c2dc905668a6902a0b4f3e6dcc281f8dd07'

    @_app.route("/status", methods=["GET"])
    def status():
        return jsonify({
            "status": "healthy"
        })

    @_app.route("/", methods=["GET"])
    def index():
        # print(request.host_url)
        username: str = ""
        if "username" in session.keys():
            username = session["username"]
        return render_template("index.html", username=username)
    
    @_app.route("/signup", methods=["GET"])
    def signup():
        username: str = ""
        error: str = ""
        if "username" in session.keys():
            username = session["username"]
        if "error" in session.keys():
            error = session.pop("error")
        return render_template("signup.html", username=username, error=error)
    
    @_app.route("/signingup", methods=["GET", "POST"])
    def signingup():
        if request.method == "GET": return redirect(url_for("signup"))

        username = request.form["username"]
        username_taken: bool = username.lower() in DataInstance().db().keys()
        if not username_taken:
            DataInstance().db()[username.lower()] = {
                "username": username,
                "password": hashpw(request.form["password"].encode(), gensalt()).decode(),
                "preferred_choice": request.form["preferred_choice"],
                "total_wins": 0,
                "total_loses": 0,
                "total_draws": 0,
                "queue": [],
                "games": []
            }
            DataInstance().commit_db()
        
        if username_taken:
            session["error"] = "Username Taken"
            return redirect(url_for("signup"))
        session["username"] = username
        return redirect(url_for("login"))
    
    @_app.route("/login", methods=["GET"])
    def login():
        username: str = ""
        error: str = ""
        if "username" in session.keys():
            username = session["username"]
        if "error" in session.keys():
            error = session.pop("error")
        return render_template("login.html", username=username, error=error)
    
    @_app.route("/loggingin", methods=["GET", "POST"])
    def loggingin():
        if request.method == "GET": 
            return redirect(url_for("login"))
        username: str = request.form["username"]
        password: str = request.form["password"]

        session["username"] = username
        if (
            not username.lower() in DataInstance().db().keys()
        ) or (
            not checkpw(
                password.encode(), 
                DataInstance().db()[username.lower()]["password"].encode()
            )
        ):
            session["error"] = "Username/Password Incorrect"
            return redirect(url_for("login"))
        return redirect(url_for("index"))
    
    @_app.route("/logout", methods=["GET"])
    def logout():
        return redirect(url_for("session_clear"))
    
    @_app.route("/battle", methods=["GET"])
    def battle():
        username: str = ""
        outcome: str = ""
        error: str = ""
        if not "username" in session.keys(): return redirect(url_for("login"))
        username = session["username"]

        if "outcome" in session.keys():
            outcome = session.pop("outcome")

        if "error" in session.keys():
            error = session.pop("error")

        return render_template("battle.html", username=username, outcome=outcome, error=error)
    
    @_app.route("/battling", methods=["GET", "POST"])
    def battling():
        if request.method == "GET": return redirect(url_for("battle"))

        username: str = ""
        if not "username" in session.keys(): return redirect(url_for("login"))
        username = session["username"]
        user_choice = request.form["choice"]

        other_username = request.form["opponent"]
        other_choice = ""

        user_queue: List[Dict[str, str]] = DataInstance().db()[username.lower()]["queue"]
        outcome: int = -42
        
        if username.lower() == other_username.lower(): 
            session["error"] = "Cannot battle yourself"
            return redirect(url_for("battle"))

        if len(other_username) == 0:
            if len(user_queue) == 0: 
                other_username = "RoboPlayer"
                other_choice = choice(["rock", "paper", "scissor"])
                outcome = determine_winner(user_choice, other_choice)
            else:
                other = user_queue.pop(0)
                other_username = other["opponent"]
                other_choice = other["opp_choice"]
                outcome = determine_winner(user_choice, other_choice)
        else:
            for i, battle in enumerate(user_queue):
                if battle["opponent"] == other_username.lower():
                    user_queue.pop(i)
                    other_choice = battle["opp_choice"]
                    outcome = determine_winner(user_choice, other_choice)

            if not other_username.lower() in DataInstance().db().keys():
                session["error"] = "Username not found in system"
                return redirect(url_for("battle"))
            
        if outcome == -1:
            DataInstance().db()[username.lower()]["total_loses"] += 1
            DataInstance().db()[other_username.lower()]["total_wins"] += 1
            session["outcome"] = (outcome, f"You lost to {other_choice}")
        elif outcome == 0:
            DataInstance().db()[username.lower()]["total_draws"] += 1
            DataInstance().db()[other_username.lower()]["total_draws"] += 1
            session["outcome"] = (outcome, f"You drew with {other_choice}")
        elif outcome == 1:
            DataInstance().db()[username.lower()]["total_wins"] += 1
            DataInstance().db()[other_username.lower()]["total_loses"] += 1
            session["outcome"] = (outcome, f"You won over {other_choice}")
        elif outcome == -42:
            DataInstance().db()[other_username.lower()]["queue"].append({
                "opponent": username,
                "opp_choice": user_choice
            })
            DataInstance().commit_db()
            return redirect(url_for("history"))
        
        DataInstance().db()[username.lower()]["games"].insert(
            0, {
                "choice": user_choice,
                "opponent": other_username,
                "opp_choice": other_choice,
                "result": "W" if outcome == 1 else "L" if outcome == -1 else "D"
            }
        )
        DataInstance().db()[other_username.lower()]["games"].insert(
            0, {
                "choice": other_choice,
                "opponent": username,
                "opp_choice": user_choice,
                "result": "W" if outcome == -1 else "L" if outcome == 1 else "D"
            }
        )
        DataInstance().commit_db()

        return redirect(url_for("battle"))
    
    @_app.route("/history", methods=["GET"])
    def history():
        username: str = ""
        if not "username" in session.keys(): return redirect(url_for("login"))
        username = session["username"]
        queue = DataInstance().db()[username.lower()]["queue"]
        history = DataInstance().db()[username.lower()]["games"]
        return render_template("history.html", username=username, queue=queue, games=history)
    
    @_app.route("/session_clear", methods=["GET"])
    def session_clear():
        session.clear()
        return redirect(url_for("index"))


    _app.wsgi_app = ProxyFix(_app.wsgi_app)
    return _app
