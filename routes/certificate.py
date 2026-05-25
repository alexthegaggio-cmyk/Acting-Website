import database
from flask import Blueprint, render_template, session
from services.auth_service import login_required
from services.module_service import get_progress

certificate_bp = Blueprint("certificate", __name__)


@certificate_bp.route("/certificate")
@login_required
def certificate_route():
    user_id = session["user_id"]
    progress = get_progress(user_id)
    all_passed = all(m["quiz_passed"] for m in progress)
    if not all_passed:
        return render_template("certificate.html", unlocked=False)
    user = database.get_user_by_id(user_id)
    return render_template(
        "certificate.html",
        unlocked=True,
        first_name=user["first_name"],
        last_name=user["last_name"],
    )
