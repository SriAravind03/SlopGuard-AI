import logging
import os
import time
from collections import defaultdict, deque
from threading import Lock
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Blueprint, Flask, flash, redirect, render_template, url_for
from flask_login import current_user
from sqlalchemy import text

from config import Config
from extensions import csrf, db, login_manager
from models.database import User
from routes.analyzer import analyzer_bp
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    if not app.config.get("SECRET_KEY") or app.config["SECRET_KEY"] == "dev-only-change-me":
        if not app.testing:
            logging.warning("SECRET_KEY is unset; using development fallback. Set SECRET_KEY before deployment.")
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please sign in to access that page."
    login_manager.login_message_category = "error"
    rate_windows = defaultdict(deque)
    rate_lock = Lock()

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    main = Blueprint("main", __name__)

    @main.get("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.home"))
        return render_template("index.html")

    @main.get("/about")
    def about():
        return render_template("about.html")

    @main.get("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ok"}, 200
        except Exception:
            db.session.rollback()
            return {"status": "unavailable"}, 503

    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(analyzer_bp)

    @app.before_request
    def limit_mutating_requests():
        from flask import request, jsonify
        if request.method != "POST":
            return None
        now = time.monotonic()
        identity = request.remote_addr or "unknown"
        bucket = f"{identity}:{request.endpoint or request.path}"
        limit = 8 if request.endpoint in {"auth.login", "auth.register"} else 12
        with rate_lock:
            recent = rate_windows[bucket]
            while recent and now - recent[0] >= 60:
                recent.popleft()
            if len(recent) >= limit:
                response = jsonify(error="Too many requests. Please wait a minute and try again.")
                response.status_code = 429
                response.headers["Retry-After"] = "60"
                return response
            recent.append(now)
        return None

    @app.errorhandler(413)
    def too_large(_error):
        flash("Request exceeds the 1 MB limit.", "error")
        return redirect(url_for("analyzer.index")), 413

    @app.after_request
    def security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("Content-Security-Policy", "default-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; connect-src 'self'")
        return response

    with app.app_context():
        db.create_all()
    return app


app = create_app()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
