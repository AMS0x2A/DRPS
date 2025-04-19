from data_instance import DataInstance
from flask import request, redirect, session, url_for
from random import choice
from typing import Dict, List, Literal, Optional, Self


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


def post_outcome(username: str, user_choice: Literal["rock", "paper", "scissors"], 
                 opp_username: str, opp_choice: Literal["rock", "paper", "scissors"],
                 outcome: int):
    if outcome == -1:
        DataInstance().user_lost(username, user_choice, opp_username, opp_choice)
        DataInstance().user_won(opp_username, opp_choice, username, user_choice)
        session["outcome"] = (outcome, f"You lost to {opp_choice}")
    elif outcome == 0:
        DataInstance().user_drew(username, user_choice, opp_username, opp_choice)
        DataInstance().user_drew(opp_username, opp_choice, username, user_choice)
        session["outcome"] = (outcome, f"You drew with {opp_choice}")
    elif outcome == 1:
        DataInstance().user_won(username, user_choice, opp_username, opp_choice)
        DataInstance().user_lost(opp_username, opp_choice, username, user_choice)
        session["outcome"] = (outcome, f"You won over {opp_choice}")


class Battling(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(Battling, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
        if request.method == "GET": return redirect(url_for("battle"))

        username: str = session["username"]
        user_choice: Literal["rock", "paper", "scissors"] = request.form["choice"]

        other_username: str = request.form["opponent"]
        other_choice: Literal["rock", "paper", "scissors", ""] = ""

        user_queue: List[Dict[str, str]] = DataInstance().db()[username.lower()]["queue"]
        outcome: int = -42
        
        if username.lower() == other_username.lower(): 
            session["error"] = "Cannot battle yourself"
            return redirect(url_for("battle"))
        
        if not DataInstance().user_exists(other_username):
            session["error"] = "Opponent not found in system"
            return redirect(url_for("battle"))

        if len(other_username) == 0 and len(user_queue) == 0: 
            other_username = "RoboPlayer"
            if not DataInstance().user_exists(other_username): 
                DataInstance().create_user(other_username, "none")
            other_choice = choice(["rock", "paper", "scissor"])
            outcome = determine_winner(user_choice, other_choice)
        elif len(other_username) == 0 and len(user_queue) > 0:
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

            if outcome == -42:
                DataInstance().db()[other_username.lower()]["queue"].append({
                    "opponent": username,
                    "opp_choice": user_choice
                })
                DataInstance().commit_db()

                session["outcome"] = f"You challenged {other_username} to battle"
                return redirect(url_for("battle"))
            
        return redirect(url_for("battle"))
