from werkzeug.security import generate_password_hash, check_password_hash

from project.models import User,Major, Comment, Survey, Favourite


def test_user_model_fields():
    user = User(
        username="testuser",
        email="test@example.com"
    )
    user.set_password("Password123")

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password_hash != "Password123"
    assert user.check_password("Password123") is True
    assert user.check_password("wrongpassword") is False

def test_major_model_fields():
    major = Major(
        name="Data Science",
        description="Test description"
    )

    assert major.name == "Data Science"
    assert major.description == "Test description"


def test_comment_model_fields():
    comment = Comment(
        content="This is a test comment.",
        user_id=1,
        major_id=1
    )

    assert comment.content == "This is a test comment."
    assert comment.user_id == 1
    assert comment.major_id == 1




def test_survey_model_fields():
    survey = Survey(
        user_id=1,
        q1="Computer Science",
        q2="Good job opportunities",
        q3="Career prospects",
        q4="Programming and software development",
        q5="Courses",
        q6="Maybe",
        q7="Yes"
    )

    assert survey.user_id == 1
    assert survey.q1 == "Computer Science"
    assert survey.q7 == "Yes"


    def test_favourite_model_fields():
        favourite = Favourite(
            user_id=1,
            major_id=1
        )

        assert favourite.user_id == 1
        assert favourite.major_id == 1
