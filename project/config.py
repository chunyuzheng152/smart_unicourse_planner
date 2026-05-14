import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(basedir, ".."))


load_dotenv(os.path.join(project_root, ".env"))

default_db_path = "sqlite:///" + os.path.join(basedir, "app.db").replace("\\", "/")

def get_database_url():
    db_url = os.environ.get("APP_DATABASE_URL")

    if db_url and db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////"):
        relative_path = db_url.replace("sqlite:///", "", 1)
        absolute_path = os.path.abspath(os.path.join(project_root, relative_path))
        return "sqlite:///" + absolute_path.replace("\\", "/")

    return db_url or default_db_path


class Config:
    SECRET_KEY = os.environ.get("APP_SECRET_KEY") 
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not SECRET_KEY:
        raise RuntimeError("APP_SECRET_KEY is missing. Please set it in .env.")