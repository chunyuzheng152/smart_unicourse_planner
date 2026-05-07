from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

project = Flask(__name__)
db = SQLAlchemy(project)
migrate = Migrate(project, db)

from project import models, app