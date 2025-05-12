from fetch import app, db

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    player_id = db.Column(db.String(200), unique=True, nullable=False)
