from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect

from project import db, migrate
from project.config import Config
from project.models import User, Survey
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

db.init_app(app)
csrf = CSRFProtect(app)


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

    return render_template("settings.html", user=user)

@app.route("/computer-science")
def computer_science():
    return render_template("computer_science.html")


@app.route("/data-science")
def data_science():
    return render_template("data_science.html")


@app.route("/software-engineering")
def software_engineering():
    return render_template("software_engineering.html")


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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

