from os import getenv, path
from dotenv import load_dotenv

from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

basedir = path.abspath(path.dirname(__file__))


class Config(object):
    SECRET_KEY = getenv("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI") or \
        "sqlite:///" + path.join(basedir, "app.db")
    STRIPE_PUBLIC_KEY = getenv("STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = getenv("STRIPE_SECRET_KEY")
    STRIPE_PLAN_ID = getenv("STRIPE_PLAN_ID")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
