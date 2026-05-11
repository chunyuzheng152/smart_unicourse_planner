from flask import Config, Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from project.config import Config

project = Flask(__name__)
project.config.from_object(Config)
db = SQLAlchemy(project)
migrate = Migrate(project, db)

from project import app