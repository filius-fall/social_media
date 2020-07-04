from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile("config.py")
app.config.from_object("config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
