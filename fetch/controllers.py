from fetch import db
import requests
from flask import jsonify, session, render_template, redirect, url_for, flash
from fetch.forms import LoginForm, SignupForm, SettingsForm
from werkzeug.security import check_password_hash, generate_password_hash  # Import password hash checker
from fetch.models import RestrictedFriends, Stats, User  # Import your User model
from flask_login import login_required, current_user, login_user, logout_user
 
def try_login(username, password):
    user = User.query.filter_by(username=username).first()
    #validtate user and password
    if user and check_password_hash(user.password, password):
        return user
    else:
        return "Invalid username or password"
 
def try_signup(username, password, player_id):
 
        if not player_id.isdigit() or len(player_id) != 9:
            return "Player ID must be exactly 9 digits."
 
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists. Please choose something else.'
       
        # Check if the playerid already is connected to an account
        existing_player = User.query.filter_by(player_id=player_id).first()
        if existing_player:
            return "That Player ID is already linked to another account."
 
        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(password)
 
        # Create a new user with the hashed password and add to the database
        new_user = User(username=username, password=hashed_password, player_id=player_id)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"
        return new_user
   
def try_change_settings(new_username=None, new_password=None, new_playerID=None, data_sharing=True, restricted_friends=None, user=None):
 
            if new_username:
                existing_user = User.query.filter_by(username=new_username).first()
                if existing_user:
                    return 'Username already exists. Please choose something else.'
                user.username = new_username
            if new_password:
                user.password = generate_password_hash(new_password)
            if new_playerID:
                existing_player = User.query.filter_by(player_id=new_playerID).first()
                if existing_player:
                    return "That Player ID is already linked to another account."
                if not new_playerID.isdigit() or ( (len(new_playerID) != 9) and (len(new_playerID) != 10)):
                    return "Player ID must be exactly 9 or 10 digits."
                user.player_id = new_playerID
 
            rf = RestrictedFriends.query.filter_by(player_id=user.player_id).first()
            if not rf:
                rf = RestrictedFriends(player_id=user.player_id)
                db.session.add(rf)
 
            rf.data_sharing = data_sharing
            rf.restricted_friends = restricted_friends
 
            db.session.commit()
            #updating the login details
            return user