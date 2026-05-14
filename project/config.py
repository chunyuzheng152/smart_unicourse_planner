import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(basedir, ".."))

# Load environment variables from .env in the project root
load_dotenv(os.path.join(project_root, ".env"))

default_db_path = "sqlite:///" + os.path.join(basedir, "app.db")


class Config:
    SECRET_KEY = os.environ.get("APP_SECRET_KEY") or "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("APP_DATABASE_URL") or default_db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False