def test_security_headers(client):
    response = client.get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_csrf_protection_enabled_by_default(tmp_path):
    from app import create_app
    app = create_app({"TESTING": False, "SECRET_KEY": "test", "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'csrf.db'}"})
    response = app.test_client().post("/login", data={"identity":"x", "password":"x"})
    assert response.status_code == 400
