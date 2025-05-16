import os

basedir = os.path.dirname(os.path.abspath(__file__))
default_database_location = "sqlite:///" + os.path.join(basedir, "fetch.db")

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_database_location
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
