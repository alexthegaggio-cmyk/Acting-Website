import os
from flask import Blueprint, request, render_template, session, redirect, url_for, flash, current_app, jsonify
import json
from services.auth_service import login_required
from services.module_service import check_unlock, get_progress, grade_quiz, get_quiz, get_monologues, get_improv_scenes, get_emotion_scripts, get_audition_scripts
import database

modules_bp = Blueprint("modules", __name__)

ALLOWED_EXTENSIONS = {"mp4", "mov", "webm", "mkv", "avi", "blob"}

def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@modules_bp.route("/module/<int:n>")
@login_required
def module_route(n):
    if n < 1 or n > 5:
        return redirect(url_for("dashboard.dashboard_route"))
    user_id = session["user_id"]
    if not check_unlock(user_id, n):
        flash("Complete the previous module first.", "error")
        return redirect(url_for("dashboard.dashboard_route"))
    progress = get_progress(user_id)
    module = progress[n - 1]
    quiz_questions = get_quiz(n)
    
    # Get specific scripts based on module number
    scripts = []
    if n == 2:
        scripts = get_monologues()
    elif n == 3:
        scripts = get_improv_scenes()
    elif n == 4:
        scripts = get_emotion_scripts()
    elif n == 5:
        scripts = get_audition_scripts()

    return render_template("module.html", module=module, module_number=n, quiz_questions=quiz_questions, scripts=scripts)

@modules_bp.route("/module/<int:n>/notes", methods=["POST"])
@login_required
def save_notes_route(n):
    if n < 1 or n > 5:
        return redirect(url_for("dashboard.dashboard_route"))
    user_id = session["user_id"]
    if not check_unlock(user_id, n):
        flash("Complete the previous module first.", "error")
        return redirect(url_for("dashboard.dashboard_route"))
    if request.is_json:
        notes = request.json.get("notes", "").strip()
    else:
        notes = request.form.get("notes", "").strip()
        
    database.save_notes(user_id, n, notes)
    
    if request.is_json:
        return jsonify({"success": True})
        
    flash("Notes saved.", "success")
    return redirect(url_for("modules.module_route", n=n))

@modules_bp.route("/module/<int:n>/quiz", methods=["POST"])
@login_required
def quiz_route(n):
    if n < 1 or n > 5:
        return redirect(url_for("dashboard.dashboard_route"))
    user_id = session["user_id"]
    if not check_unlock(user_id, n):
        flash("Complete the previous module first.", "error")
        return redirect(url_for("dashboard.dashboard_route"))
    submitted = request.form.to_dict()
    result = grade_quiz(user_id, n, submitted)
    
    if request.headers.get("Accept") and "application/json" in request.headers.get("Accept"):
        return jsonify(result)
        
    if result["passed"]:
        flash(f"Quiz passed — {result['score']}%!", "success")
    else:
        flash(f"Quiz not passed — {result['score']}%. 95% needed.", "error")
    return redirect(url_for("modules.module_route", n=n))

@modules_bp.route("/module/<int:n>/submit", methods=["POST"])
@login_required
def submit_route(n):
    if n < 1 or n > 5:
        return redirect(url_for("dashboard.dashboard_route"))
    user_id = session["user_id"]
    if not check_unlock(user_id, n):
        flash("Complete the previous module first.", "error")
        return redirect(url_for("dashboard.dashboard_route"))

    if "video" not in request.files:
        flash("No file uploaded.", "error")
        return redirect(url_for("modules.module_route", n=n))

    file = request.files["video"]
    if file.filename == "" or not _allowed_file(file.filename):
        flash("Invalid file type. Only mp4, mov, webm accepted.", "error")
        return redirect(url_for("modules.module_route", n=n)), 400

        
    uploads_dir = os.path.join(current_app.static_folder, "uploads")
    filename = f"user{user_id}_mod{n}.{file.filename.rsplit('.', 1)[1].lower()}"
    file_path = os.path.join(uploads_dir, filename)
    file.save(file_path)

    database.save_submission(user_id, n, file_path)
    flash("Submission received.", "success")
    return redirect(url_for("modules.module_route", n=n))
