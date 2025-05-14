from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign in')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    player_id = StringField('Player ID', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class SettingsForm(FlaskForm):
    new_username = StringField('New Username', validators=[DataRequired()])
    new_player_id = StringField('New Player ID', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8)])
    allow_friend_sharing = BooleanField('Allow Friend Sharing')

    # Multiple submit buttons
    update_settings = SubmitField('Update Settings')  # corresponds to SettingsForm
    save_friends = SubmitField('Save Settings')       # corresponds to FriendsForm
    logout = SubmitField('Logout')                    # corresponds to LogoutForm
    close_account = SubmitField('Close')