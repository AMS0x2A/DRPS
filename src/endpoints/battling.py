from data_instance import DataInstance
from flask import request, redirect, session, url_for
from random import choice
from typing import Dict, List, Optional, Self


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


class Battling(object):
    _instance: Optional[Self] = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super(Battling, cls).__new__(cls)
        return cls._instance
    
    def endpoint(cls) -> str:
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
