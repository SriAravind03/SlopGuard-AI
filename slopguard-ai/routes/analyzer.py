from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from config import Config
from detection.openai_analyzer import analyze_with_openai
from detection.scoring_engine import analyze_text
from extensions import db
from models.database import Scan
from scraper.url_scraper import ScrapeError, fetch_article

analyzer_bp = Blueprint("analyzer", __name__)


def _save(input_type, text, result, source_url=None):
    scan = Scan(user_id=current_user.id, input_type=input_type, original_text=text, source_url=source_url,
        content_quality_score=result["content_quality_score"], slop_pattern_score=result["slop_pattern_score"],
        classification=result["classification"], analysis_result=result)
    db.session.add(scan)
    db.session.commit()
    return scan


@analyzer_bp.get("/analyzer")
@login_required
def index():
    return render_template("analyzer.html")


@analyzer_bp.post("/analyze/text")
@login_required
def text():
    content = request.form.get("text", "")
    try:
        result = analyze_text(content)
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("analyzer.index"))
    if request.form.get("ai_review") == "1":
        result["optional_review"] = analyze_with_openai(content)
    scan = _save("text", content, result)
    return redirect(url_for("analyzer.results", scan_id=scan.id))


@analyzer_bp.post("/analyze/url")
@login_required
def url():
    target = request.form.get("url", "").strip()
    try:
        article = fetch_article(target)
        result = analyze_text(article["text"])
    except (ScrapeError, ValueError) as exc:
        flash(str(exc), "error")
        return redirect(url_for("analyzer.index"))
    result["source_title"] = article["title"]
    scan = _save("url", article["text"], result, article["url"])
    return redirect(url_for("analyzer.results", scan_id=scan.id))


@analyzer_bp.get("/results/<int:scan_id>")
@login_required
def results(scan_id):
    scan = current_user.scans.filter_by(id=scan_id).first_or_404()
    return render_template("results.html", scan=scan, data=scan.analysis_result, timestamp=scan.created_at or datetime.now(timezone.utc))
