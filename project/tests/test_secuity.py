from werkzeug.security import generate_password_hash, check_password_hash


def test_signup_form_has_csrf_token(client):
    response = client.get("/signup")
    html = response.data.decode()

    assert 'name="csrf_token"' in html


def test_login_form_has_csrf_token(client):
    response = client.get("/login")
    html = response.data.decode()

    assert 'name="csrf_token"' in html


def test_survey_form_has_csrf_token(client):
    response = client.get("/survey")
    html = response.data.decode()

    assert 'name="csrf_token"' in html


def test_comment_form_has_csrf_token(client):
    response = client.get("/data-science")
    html = response.data.decode()

    assert 'name="csrf_token"' in html


def test_password_hash_is_not_plain_text():
    password = "Password123"
    hashed_password = generate_password_hash(password)

    assert hashed_password != password


def test_password_hash_can_be_checked():
    password = "Password123"
    hashed_password = generate_password_hash(password)

    assert check_password_hash(hashed_password, password) is True
    assert check_password_hash(hashed_password, "wrongpassword") is False