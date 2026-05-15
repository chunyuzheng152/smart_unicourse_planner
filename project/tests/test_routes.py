import uuid

def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_signup_page_loads(client):
    response = client.get("/signup")
    assert response.status_code == 200


def test_settings_page_redirects_when_not_logged_in(client):
    response = client.get("/settings", follow_redirects=False)

    assert response.status_code in [302, 303]
    assert "/login" in response.headers["Location"]


def test_survey_page_loads(client):
    response = client.get("/survey")
    assert response.status_code == 200


def test_major_pages_load(client):
    pages = [
        "/computer-science",
        "/data-science",
        "/software-engineering",
    ]

    for page in pages:
        response = client.get(page)
        assert response.status_code == 200


def test_login_post_invalid_user_redirects_to_login(client):
    response = client.post(
        "/login",
        data={
            "username": "this_user_should_not_exist",
            "password": "WrongPassword123"
        },
        follow_redirects=False
    )

    assert response.status_code in [302, 303]
    assert "/login" in response.headers["Location"]


def test_signup_post_redirects_to_login(client):
    unique_id = uuid.uuid4().hex[:8]

    response = client.post(
        "/signup",
        data={
            "username": f"testuser_{unique_id}",
            "email": f"test_{unique_id}@example.com",
            "password": "Password123",
            "repeat_password": "Password123"
        },
        follow_redirects=False
    )

    assert response.status_code in [302, 303]
    assert "/login" in response.headers["Location"]



def test_survey_post_accepts_all_answers(client):
    response = client.post(
        "/survey",
        data={
            "q1": "Computer Science",
            "q2": "Good job opportunities",
            "q3": "Career prospects",
            "q4": "Programming and software development",
            "q5": "Courses",
            "q6": "Maybe",
            "q7": "Yes",
        },
        follow_redirects=False
    )

    assert response.status_code in [200, 302, 303]


def test_comment_post_for_data_science_redirects_to_login_when_not_logged_in(client):
    response = client.post(
        "/add-comment",
        data={
            "content": "This is a test comment.",
            "major_slug": "data-science"
        },
        follow_redirects=False
    )

    assert response.status_code in [302, 303]
    assert "/login" in response.headers["Location"]



def test_empty_comment_post_redirects_to_login_when_not_logged_in(client):
    response = client.post(
        "/add-comment",
        data={
            "content": "",
            "major_slug": "data-science"
        },
        follow_redirects=False
    )

    assert response.status_code in [302, 303]
    assert "/login" in response.headers["Location"]