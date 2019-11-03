from os import getenv, path
from dotenv import load_dotenv

load_dotenv()

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    SECRET_KEY = getenv("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "app.db")
    STRIPE_PUBLIC_KEY = getenv("STRIPE_PUBLIC_KEY") or "PUBLIC_KEY"
    STRIPE_SECRET_KEY = getenv("STRIPE_SECRET_KEY") or "SECRET_KEY"
    STRIPE_PLAN_ID = getenv("STRIPE_PLAN_ID") or "PLAN_ID"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DROPZONE_ALLOWED_FILE_CUSTOM = True
    DROPZONE_ALLOWED_FILE_TYPE = '.csv'
    PERMANENT_SESSION_LIFETIME = True
    STREETVIEW_KEY = getenv("STREETVIEW_KEY") or 'API_KEY'
