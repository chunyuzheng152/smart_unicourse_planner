from project import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    emailAddress = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.LargeBinary, nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    major = db.Column(db.String(50), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)
    q3 = db.Column(db.Integer, nullable=False)
    q4 = db.Column(db.Integer, nullable=False)
    q5 = db.Column(db.Integer, nullable=False)
    q6 = db.Column(db.Integer, nullable=False)
    q7 = db.Column(db.Integer, nullable=False)