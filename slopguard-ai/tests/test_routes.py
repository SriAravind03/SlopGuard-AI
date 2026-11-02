from models.database import User


def register(client):
    return client.post("/register", data={"username":"tester", "email":"t@example.com", "password":"correct-horse-1"}, follow_redirects=True)


def test_registration_login_analysis_and_history(client, app):
    response = register(client)
    assert response.status_code == 200
    assert b"Good to see you" in response.data
    result = client.post("/analyze/text", data={"text":"A measured report describes 15 samples collected in June. Data and methods are linked for review."}, follow_redirects=True)
    assert result.status_code == 200
    assert b"Analysis results" in result.data
    assert b"Scoring Method" not in result.data
    assert client.get("/history").status_code == 200


def test_auth_and_password_hash(client, app):
    assert client.get("/dashboard").status_code == 302
    register(client)
    with app.app_context():
        user = User.query.first()
        assert user.password_hash != "correct-horse-1"
        assert user.check_password("correct-horse-1")


def test_health_route(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_empty_text_has_friendly_error(client):
    register(client)
    response = client.post("/analyze/text", data={"text":"  "}, follow_redirects=True)
    assert b"Enter some text to analyze" in response.data


def test_settings_password_change(client):
    register(client)
    response = client.post("/settings", data={"current_password":"correct-horse-1", "new_password":"another-horse-22", "confirm_password":"another-horse-22"}, follow_redirects=True)
    assert b"Password updated" in response.data
