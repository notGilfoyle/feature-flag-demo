import hashlib
import json

from fastapi import FastAPI

app = FastAPI(title="Feature Flag Demo")


def load_flags():
    with open("flags.json", "r") as f:
        return json.load(f)


def is_beta_user(username: str, flags: dict) -> bool:
    return username in flags["beta_users"]


def is_in_rollout(username: str, percentage: int) -> bool:
    """
    Stable rollout.

    Same user always gets the same result.
    """
    value = int(hashlib.md5(username.encode()).hexdigest(), 16)
    bucket = value % 100
    return bucket < percentage


@app.get("/")
def home():
    return {
        "message": "Feature Flag Demo API"
    }


@app.get("/dashboard/{username}")
def dashboard(username: str):
    flags = load_flags()

    if flags["new_dashboard"]:
        dashboard = "New Dashboard"
    else:
        dashboard = "Old Dashboard"

    return {
        "user": username,
        "dashboard": dashboard
    }


@app.get("/theme/{username}")
def theme(username: str):
    flags = load_flags()

    return {
        "user": username,
        "theme": "Dark" if flags["dark_mode"] else "Light"
    }


@app.get("/beta/{username}")
def beta(username: str):
    flags = load_flags()

    if is_beta_user(username, flags):
        return {
            "feature": "AI Assistant",
            "enabled": True
        }

    return {
        "feature": "AI Assistant",
        "enabled": False
    }


@app.get("/rollout/{username}")
def rollout(username: str):
    flags = load_flags()

    enabled = is_in_rollout(
        username,
        flags["rollout_percentage"]
    )

    return {
        "user": username,
        "new_search_enabled": enabled
    }