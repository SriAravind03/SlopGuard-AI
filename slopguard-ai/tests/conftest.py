import pytest

from app import create_app
from extensions import db


@pytest.fixture
def app(tmp_path):
    test_app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False, "SECRET_KEY": "test-key", "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}"})
    with test_app.app_context():
        db.drop_all()
        db.create_all()
    yield test_app
    with test_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
