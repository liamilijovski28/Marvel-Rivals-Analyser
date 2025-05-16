from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from fetch.config import DevelopmentConfig, TestingConfig
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
login.login_view = 'main.login'

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from fetch.blueprints import blueprint
    from fetch.models import User
    app.register_blueprint(blueprint)
    csrf = CSRFProtect(app)

    @login.user_loader
    def load_user(player_id):
        return User.query.get(player_id)
    return app
