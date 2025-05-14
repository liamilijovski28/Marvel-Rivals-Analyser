from fetch import app, db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    player_id = db.Column(db.String(12), primary_key=True, unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Indicates if the user is active

    stats = db.relationship('Stats', back_populates='user', uselist=False)
    friends = db.relationship('Friends', back_populates='user')

    def get_id(self):
        return self.player_id

class Stats(db.Model):
    player_id = db.Column(db.String(80), db.ForeignKey('user.player_id'), primary_key=True, nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    matches_played = db.Column(db.Integer, default=0)
    win_rate = db.Column(db.Float, default=0.0)
    Kd = db.Column(db.Float, default=0.0)

    user = db.relationship('User', back_populates='stats')

class Friends(db.Model):
    player_id = db.Column(db.String(80), db.ForeignKey('user.player_id'), primary_key=True, nullable=False)
    friend_list = db.Column(db.PickleType, nullable=True)  # Stores a list of friend player IDs
    allow_friend_sharing = db.Column(db.Boolean, default=False)  # Indicates if friend sharing is allowed

    user = db.relationship('User', back_populates='friends')
    