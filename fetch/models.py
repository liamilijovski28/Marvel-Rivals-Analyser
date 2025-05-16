from fetch import db
from flask_login import UserMixin

# --- Association table for accepted friends ---
friend_association = db.Table('friends',
    db.Column('user_id', db.String(80), db.ForeignKey('user.username')),
    db.Column('friend_id', db.String(80), db.ForeignKey('user.username'))
)

# --- FriendRequest model ---
class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    receiver_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# --- User model ---
class User(UserMixin, db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    player_id = db.Column(db.String(12), primary_key=True, unique=True, nullable=False)

    stats = db.relationship('Stats', back_populates='user', uselist=False, cascade="all, delete-orphan")
    restricted_friends = db.relationship('RestrictedFriends', back_populates='user', uselist=False, cascade="all, delete-orphan")

    # NEW: many-to-many relationship with other users
    friends = db.relationship(
        'User',
        secondary=friend_association,
        primaryjoin=username == friend_association.c.user_id,
        secondaryjoin=username == friend_association.c.friend_id,
        backref='added_by'
    )

    def get_id(self):
        return self.player_id

# --- Stats model ---
class Stats(db.Model):
    player_id = db.Column(db.String(80), db.ForeignKey('user.player_id'), primary_key=True, nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    matches_played = db.Column(db.Integer, default=0)
    win_rate = db.Column(db.Float, default=0.0)
    Kd = db.Column(db.Float, default=0.0)

    user = db.relationship('User', back_populates='stats')

# --- Restricted friends/data-sharing settings ---
class RestrictedFriends(db.Model):
    player_id = db.Column(db.String(80), db.ForeignKey('user.player_id'), primary_key=True, nullable=False)
    restricted_friends = db.Column(db.String(200))
    data_sharing = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='restricted_friends')
