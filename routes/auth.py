from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from services.auth_service import register, login, logout

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "POST":
        result = register(
            first_name=request.form.get("first_name", "").strip(),
            last_name=request.form.get("last_name", "").strip(),
            email=request.form.get("email", "").strip(),
            password=request.form.get("password", ""),
            confirm=request.form.get("confirm", ""),
        )
        if result["success"]:
            flash("Account created — please log in.", "success")
            return redirect(url_for("auth.login_route"))
        flash(result["error"], "error")
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        result = login(
            email=request.form.get("email", "").strip(),
            password=request.form.get("password", ""),
        )
        if result["success"]:
            return redirect(url_for("dashboard.dashboard_route"))
        flash(result["error"], "error")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout_route():
    logout()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login_route"))
