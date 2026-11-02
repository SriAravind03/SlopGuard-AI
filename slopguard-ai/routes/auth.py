import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_
from urllib.parse import urlsplit

from extensions import db
from models.database import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))
    if request.method == "POST":
        username, email, password = (request.form.get(k, "").strip() for k in ("username", "email", "password"))
        error = None
        if not re.fullmatch(r"[A-Za-z0-9_.-]{3,40}", username): error = "Username must be 3–40 letters, numbers, dots, dashes, or underscores."
        elif not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email) or len(email) > 254: error = "Enter a valid email address."
        elif len(password) < 10 or len(password) > 128: error = "Password must be 10–128 characters."
        elif User.query.filter(or_(User.username.ilike(username), User.email.ilike(email))).first(): error = "That username or email is already registered."
        if error:
            flash(error, "error")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Account created. You can now analyze content.", "success")
            return redirect(url_for("dashboard.home"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))
    if request.method == "POST":
        user = User.query.filter(or_(User.username.ilike(request.form.get("identity", "").strip()), User.email.ilike(request.form.get("identity", "").strip()))).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user, remember=False, fresh=True)
            target = request.args.get("next", "")
            parsed = urlsplit(target)
            safe_target = target.startswith("/") and not target.startswith("//") and not parsed.netloc and not parsed.scheme
            return redirect(target if safe_target else url_for("dashboard.home"))
        flash("Invalid username/email or password.", "error")
    return render_template("login.html")


@auth_bp.post("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
