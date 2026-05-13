from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

from project import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    avatar_filename = db.Column(db.String(255), nullable=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    surveys = db.relationship("Survey", backref="user", lazy=True)
    favourites = db.relationship("Favourite", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)

    comments = db.relationship("Comment", backref="major", lazy=True)
    favourites = db.relationship("Favourite", backref="major", lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    major_id = db.Column(db.Integer, db.ForeignKey("major.id"), nullable=True)


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    major_id = db.Column(db.Integer, db.ForeignKey("major.id"), nullable=False)


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    q1 = db.Column(db.String(120), nullable=False)
    q2 = db.Column(db.String(120), nullable=False)
    q3 = db.Column(db.String(120), nullable=False)
    q4 = db.Column(db.String(120), nullable=False)
    q5 = db.Column(db.String(120), nullable=False)
    q6 = db.Column(db.String(120), nullable=False)
    q7 = db.Column(db.String(120), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)