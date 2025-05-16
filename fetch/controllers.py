from fetch import db
import requests
from flask import flash
from fetch.models import User, RestrictedFriends
from werkzeug.security import check_password_hash, generate_password_hash


def try_login(username, password):
    """
    Attempt to log a user in by verifying their credentials.
    """
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return "Invalid username or password"


def try_signup(username, password, player_id):
    """
    Attempt to create a new user account.
    Includes validation for duplicate usernames and player IDs.
    """
    if not player_id.isdigit() or len(player_id) != 9:
        return "Player ID must be exactly 9 digits."

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "Username already exists. Please choose something else."

    existing_player = User.query.filter_by(player_id=player_id).first()
    if existing_player:
        return "That Player ID is already linked to another account."

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, player_id=player_id)

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        return f"An error occurred while creating the user: {str(e)}"


def try_change_settings(new_username=None, new_password=None, new_playerID=None,
                        data_sharing=True, restricted_friends=None, user=None):
    """
    Change user settings such as username, password, player ID, and friend visibility.
    """
    if new_username:
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user and existing_user.id != user.id:
            return "Username already exists. Please choose something else."
        user.username = new_username

    if new_password:
        user.password = generate_password_hash(new_password)

    if new_playerID:
        if not new_playerID.isdigit() or len(new_playerID) != 9:
            return "Player ID must be exactly 9 digits."
        existing_player = User.query.filter_by(player_id=new_playerID).first()
        if existing_player and existing_player.id != user.id:
            return "That Player ID is already linked to another account."
        user.player_id = new_playerID

    rf = RestrictedFriends.query.filter_by(player_id=user.player_id).first()
    if not rf:
        rf = RestrictedFriends(player_id=user.player_id)
        db.session.add(rf)

    rf.data_sharing = data_sharing
    rf.restricted_friends = restricted_friends

    try:
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        return f"An error occurred while saving settings: {str(e)}"
