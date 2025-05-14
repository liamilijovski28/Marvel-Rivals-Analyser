from fetch import app, db

class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    player_id = db.Column(db.String(12), primary_key=True, unique=True, nullable=False)
    stats = db.relationship('Stats', back_populates='user', uselist=False)

class Stats(db.Model):
    player_id = db.Column(db.String(80), db.ForeignKey('user.player_id'), primary_key=True, nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    matches_played = db.Column(db.Integer, default=0)
    win_rate = db.Column(db.Float, default=0.0)
    Kd = db.Column(db.Float, default=0.0)

    user = db.relationship('User', back_populates='stats')