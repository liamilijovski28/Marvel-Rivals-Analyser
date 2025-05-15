from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from fetch.config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = Config.SECRET_KEY
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from fetch import models
from fetch import routes