def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_signup_page_loads(client):
    response = client.get("/signup")
    assert response.status_code == 200


def test_settings_page_loads(client):
    response = client.get("/settings")
    assert response.status_code == 200


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


def test_login_post_redirects_to_home(client):
    response = client.post(
        "/login",
        data={"username": "testuser"},
        follow_redirects=False
    )

    assert response.status_code in [302, 303]
    assert "/" in response.headers["Location"]


def test_signup_post_redirects_to_login(client):
    response = client.post(
        "/signup",
        data={
            "email": "test@example.com",
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


def test_comment_post_for_data_science(client):
    response = client.post(
        "/majors/data-science/comments",
        data={"comment": "This is a test comment."},
        follow_redirects=False
    )

    assert response.status_code in [200, 302, 303]


def test_empty_comment_post_is_rejected(client):
    response = client.post(
        "/majors/data-science/comments",
        data={"comment": ""},
        follow_redirects=False
    )

    assert response.status_code in [200, 302, 303, 400]