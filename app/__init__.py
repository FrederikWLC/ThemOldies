from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dropzone import Dropzone
import stripe

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
dropzone = Dropzone(app)
stripe.api_key = app.config["STRIPE_SECRET_KEY"]

from app import routes, models
