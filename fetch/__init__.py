from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from fetch.config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = Config.SECRET_KEY
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
from fetch.models import User, Stats
@login.user_loader
def load_user(player_id):
    return User.query.get(player_id)
from fetch import routes