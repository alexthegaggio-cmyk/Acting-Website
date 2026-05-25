from functools import wraps
from flask import session, redirect, url_for
import bcrypt
import database


def register(first_name, last_name, email, password, confirm):
    """Validate inputs, hash password, persist user."""
    if not all([first_name, last_name, email, password, confirm]):
        return {"success": False, "error": "All fields are required."}

    if password != confirm:
        return {"success": False, "error": "Passwords do not match."}

    existing = database.get_user_by_email(email)
    if existing:
        return {"success": False, "error": "An account with this email already exists."}

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    database.create_user(first_name, last_name, email, password_hash)
    return {"success": True}


def login(email, password):
    """Verify credentials, set session."""
    if not email or not password:
        return {"success": False, "error": "Email and password are required."}

    user = database.get_user_by_email(email)
    if not user:
        return {"success": False, "error": "Invalid email or password."}

    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return {"success": False, "error": "Invalid email or password."}

    session["user_id"] = user["id"]
    return {"success": True}


def logout():
    """Clear session."""
    session.clear()


def login_required(f):
    """Decorator — redirects to login if no active session."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login_route"))
        return f(*args, **kwargs)
    return decorated
