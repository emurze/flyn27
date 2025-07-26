import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    # TODO: understand why should we use it
    SQLALCHEMY_TRACK_MODIFICATIONS = False
