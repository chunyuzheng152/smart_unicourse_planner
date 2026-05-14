from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
from flask_wtf.csrf import CSRFProtect

from project import db, migrate
from project.config import Config
from project.models import User, Survey, Comment, Major, Favourite
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

UPLOAD_FOLDER = os.path.join(app.root_path, "static", "uploads", "avatars")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
db.init_app(app)
migrate.init_app(app, db)
csrf = CSRFProtect(app)

MAJOR_MAP = {
    "computer-science": {
        "name": "Computer Science",
        "endpoint": "computer_science"
    },
    "data-science": {
        "name": "Data Science",
        "endpoint": "data_science"
    },
    "software-engineering": {
        "name": "Software Engineering",
        "endpoint": "software_engineering"
    }
}


def get_or_create_major(major_slug):
    major_data = MAJOR_MAP.get(major_slug)

    if not major_data:
        return None

    major = Major.query.filter_by(name=major_data["name"]).first()

    if not major:
        major = Major(name=major_data["name"], description="")
        db.session.add(major)
        db.session.commit()

    return major


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash("Invalid username or password.")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        session["username"] = user.username
        session["avatar_filename"] = user.avatar_filename

        flash("Login successful.")
        return redirect(url_for("index"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("index"))


@app.route("/update-email", methods=["POST"])
def update_email():
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))
    
    new_email = request.form.get("new_email")

    if not new_email:
        flash("Please enter a new email.")
        return redirect(url_for("settings"))
    
    user = User.query.get(session["user_id"])

    if user is None:
        flash("User not found.")
        return redirect(url_for("login"))
    
    existing_user = User.query.filter_by(email=new_email).first()

    if existing_user and existing_user.id != user.id:
        flash("This email is already used.")
        return redirect(url_for("settings"))
    
    user.email = new_email
    db.session.commit()

    flash("Email updated successfully.")
    return redirect(url_for("settings"))


@app.route("/change-password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))
    
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if not current_password or not new_password or not confirm_password:
        flash("Please fill in all password fields.")
        return redirect(url_for("settings"))
    
    if new_password != confirm_password:
        flash("New passwords do not match.")
        return redirect(url_for("settings"))
    
    user = User.query.get(session["user_id"])

    if user is None:
        flash("User not found.")
        return redirect(url_for("login"))
    
    if not user.check_password(current_password):
        flash("Current password is incorrect.")
        return redirect(url_for("settings"))
    user.set_password(new_password)
    db.session.commit()

    flash("Password changed successfully.")
    return redirect(url_for("settings"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")

        if not username or not email or not password or not repeat_password:
            flash("Please fill in all fields.")
            return redirect(url_for("signup"))

        if password != repeat_password:
            flash("Passwords do not match.")
            return redirect(url_for("signup"))

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.")
            return redirect(url_for("signup"))

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/settings", methods=["GET", "POST"])
def settings():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in first.")
        return redirect(url_for("login"))

    user = db.session.get(User, user_id)

    if request.method == "POST":
        action = request.form.get("action")

        if action == "remove_avatar":
            if user.avatar_filename:
                old_path = os.path.join(app.config["UPLOAD_FOLDER"], user.avatar_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)

                user.avatar_filename = None
                session["avatar_filename"] = None
                db.session.commit()

            flash("Avatar removed.")
            return redirect(url_for("settings"))

        avatar = request.files.get("avatar")

        if avatar and avatar.filename:
            if not allowed_file(avatar.filename):
                flash("Only png, jpg, jpeg, and webp files are allowed.")
                return redirect(url_for("settings"))

            filename = secure_filename(avatar.filename)
            ext = filename.rsplit(".", 1)[1].lower()
            new_filename = f"user_{user.id}.{ext}"

            save_path = os.path.join(app.config["UPLOAD_FOLDER"], new_filename)
            avatar.save(save_path)

            user.avatar_filename = new_filename
            session["avatar_filename"] = new_filename
            db.session.commit()

            flash("Profile updated.")
            return redirect(url_for("settings"))

        flash("No file selected.")
        return redirect(url_for("settings"))

    my_comments = Comment.query.filter_by(user_id=user_id).order_by(Comment.created_at.desc()).all()
    return render_template("settings.html", user=user, my_comments=my_comments)  

@app.route("/toggle_favourite/<int:major_id>", methods=["POST"])
def toggle_favourite(major_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in first.")
        return redirect(url_for("login"))
    favourite = Favourite.query.filter_by(
        user_id=user_id,
        major_id=major_id
    ).first()

    if favourite:
        db.session.delete(favourite)
        flash("Removed from favourites.")
    else:
        new_favourite = Favourite(
            user_id=user_id,
            major_id=major_id
        )
        db.session.add(new_favourite)
        flash("Added to favourites.")
    db.session.commit()
    return redirect(request.referrer or url_for("index"))
    

@app.route("/computer-science")
def computer_science():
    major = get_or_create_major("computer-science")
    comments = Comment.query.filter_by(major_id=major.id).order_by(Comment.created_at.desc()).all()

    favourite_major_ids = set()
    user_id = session.get("user_id")

    if user_id:
        favourites = Favourite.query.filter_by(user_id=user_id).all()
        favourite_major_ids = {f.major_id for f in favourites}
    return render_template("computer_science.html", major=major, comments=comments,favourite_major_ids=favourite_major_ids)


@app.route("/data-science")
def data_science():
    major = get_or_create_major("data-science")
    comments = Comment.query.filter_by(major_id=major.id).order_by(Comment.created_at.desc()).all()

    favourite_major_ids = set()
    user_id = session.get("user_id")

    if user_id:
        favourites = Favourite.query.filter_by(user_id=user_id).all()
        favourite_major_ids = {f.major_id for f in favourites}
    return render_template("data_science.html", major=major, comments=comments,favourite_major_ids=favourite_major_ids)


@app.route("/software-engineering")
def software_engineering():
    major = get_or_create_major("software-engineering")
    comments = Comment.query.filter_by(major_id=major.id).order_by(Comment.created_at.desc()).all()

    favourite_major_ids = set()
    user_id = session.get("user_id")

    if user_id:
        favourites = Favourite.query.filter_by(user_id=user_id).all()
        favourite_major_ids = {f.major_id for f in favourites}
    return render_template("software_engineering.html", major=major, comments=comments, favourite_major_ids=favourite_major_ids)


@app.route("/add-comment", methods=["POST"])
def add_comment():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in before posting a comment.")
        return redirect(url_for("login"))

    content = request.form.get("content", "").strip()
    major_slug = request.form.get("major_slug")

    if not content:
        flash("Comment cannot be empty.")
        return redirect(url_for(MAJOR_MAP[major_slug]["endpoint"]) + "#discussion")

    major = get_or_create_major(major_slug)

    if not major:
        flash("Invalid major.")
        return redirect(url_for("index"))

    comment = Comment(
        content=content,
        user_id=user_id,
        major_id=major.id
    )

    db.session.add(comment)
    db.session.commit()

    flash("Comment posted.")
    return redirect(url_for(MAJOR_MAP[major_slug]["endpoint"]) + "#discussion")

@app.route("/survey", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")
        q5 = request.form.get("q5")
        q6 = request.form.get("q6")
        q7 = request.form.get("q7")

        if not all([q1, q2, q3, q4, q5, q6, q7]):
            flash("Please answer all questions.")
            return redirect(url_for("survey"))

        survey_response = Survey(
            q1=q1,
            q2=q2,
            q3=q3,
            q4=q4,
            q5=q5,
            q6=q6,
            q7=q7,
            user_id=session.get("user_id")
        )

        db.session.add(survey_response)
        db.session.commit()

        flash("Survey submitted.")
        return redirect(url_for("index"))

    return render_template("survey.html")


@app.route("/api/charts")
def api_charts():
    surveys = Survey.query.all()

    popular_major_counts = {}
    choice_reason_counts = {}

    for survey in surveys:
        popular_major_counts[survey.q1] = popular_major_counts.get(survey.q1,0) + 1
        choice_reason_counts[survey.q2] = choice_reason_counts.get(survey.q2,0) + 1

    return jsonify({
        "popular_majors":{
            "labels": list(popular_major_counts.keys()),
            "values": list(popular_major_counts.values())
        },
        "choice_reasons":{
            "labels": list(choice_reason_counts.keys()),
            "values": list(choice_reason_counts.values())
        }
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

