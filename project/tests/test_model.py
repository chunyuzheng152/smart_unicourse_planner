from werkzeug.security import generate_password_hash, check_password_hash

from models import User, Comment, Survey


def test_user_model_fields():
    user = User(
        displayName="Test User",
        emailAddress="test@example.com",
        password=generate_password_hash("Password123")
    )

    assert user.displayName == "Test User"
    assert user.emailAddress == "test@example.com"
    assert user.password != "Password123"


def test_password_hash_check():
    password = "Password123"
    password_hash = generate_password_hash(password)

    assert check_password_hash(password_hash, password) is True
    assert check_password_hash(password_hash, "wrongpassword") is False


def test_comment_model_fields():
    comment = Comment(
        major="Data Science",
        userID=1,
        comment="This is a test comment."
    )

    assert comment.major == "Data Science"
    assert comment.userID == 1
    assert comment.comment == "This is a test comment."


def test_survey_model_fields():
    survey = Survey(
        userID=1,
        q1=1,
        q2=2,
        q3=3,
        q4=4,
        q5=5,
        q6=6,
        q7=7
    )

    assert survey.userID == 1
    assert survey.q1 == 1
    assert survey.q7 == 7