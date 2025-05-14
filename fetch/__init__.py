from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from fetch.config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'change this later'
csrf = CSRFProtect(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(player_id):
    from fetch.models import User
    return User.query.get(player_id)

from fetch import models
from fetch import routes