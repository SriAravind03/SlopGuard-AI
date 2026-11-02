from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from extensions import db
from models.database import Scan

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/dashboard")
@login_required
def home():
    scans = current_user.scans.order_by(Scan.created_at.desc()).limit(6).all()
    total = current_user.scans.count()
    avg = current_user.scans.with_entities(func.avg(Scan.content_quality_score)).scalar()
    low = current_user.scans.filter(Scan.slop_pattern_score >= 60).count()
    return render_template("dashboard.html", scans=scans, total=total, average=round(avg or 0), low=low)


@dashboard_bp.get("/history")
@login_required
def history():
    scans = current_user.scans.order_by(Scan.created_at.desc()).limit(100).all()
    return render_template("history.html", scans=scans)


@dashboard_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        current = request.form.get("current_password", "")
        new = request.form.get("new_password", "")
        confirm = request.form.get("confirm_password", "")
        if not current_user.check_password(current):
            flash("Current password did not match.", "error")
        elif len(new) < 10 or len(new) > 128:
            flash("New password must be 10–128 characters.", "error")
        elif new != confirm:
            flash("New password entries do not match.", "error")
        else:
            current_user.set_password(new)
            db.session.commit()
            flash("Password updated.", "success")
            return redirect(url_for("dashboard.settings"))
    return render_template("settings.html")
