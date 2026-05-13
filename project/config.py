import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_db_path = "sqlite:///" + os.path.join(basedir, "app.db")

class Config:
    SECRET_KEY = os.environ.get("APP_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("APP_DATABASE_URL") or default_db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False