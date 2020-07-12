from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)

login = LoginManager(app)
login.login_view = "login"

app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models,errors


if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
        secure= None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD']),
            fromaddr='noreply@' + app.config['MAIL_SERVER'],
            toaddrs = app.config['ADMINS'], subject='Social_Media Failure',
            credentials=auth,secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)





