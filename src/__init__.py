import secrets
import datetime as dt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# defining the application
app = Flask(__name__)


# application configurations
app.config.update(
    SECRET_KEY=secrets.token_urlsafe(32),
    SQLALCHEMY_DATABASE_URI="sqlite:///quiz.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=True,

    # Setting session time
    # first do this in routes and login section
    # from flask import session
    # session.permanent=True
    PERMANENT_SESSION_LIFETIME=dt.timedelta(days=7)
)

# initializing the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User login manager configurations
login_manager = LoginManager(app)
# Login config for normal required Logins
login_manager.login_view = "login"
login_manager.login_message = "Please login first!"
login_manager.login_message_category = "info"
# Login config for re-authentication
login_manager.needs_refresh_message = "Please re-authenticate to access this page"
login_manager.needs_refresh_message_category = "info"

# Loading user from database
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return db.session.get(User, int(user_id))


# Adding datetime to jinja templates
@app.context_processor
def inject_datetime():
    return {'datetime': dt}

# Applications other parts
# Must stay at the bottom of the file
from . import models, forms, routs
