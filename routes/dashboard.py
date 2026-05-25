from flask import Blueprint, render_template, session
from services.auth_service import login_required
from services.module_service import get_progress
import database

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard_route():
    user_id = session["user_id"]
    # Temporary fix to correct name
    import sqlite3
    conn = sqlite3.connect(database.DB_PATH)
    conn.execute("UPDATE users SET last_name = 'Vernetti' WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    user = database.get_user_by_id(user_id)
    progress = get_progress(user_id)
    return render_template("dashboard.html", progress=progress, user=user)
