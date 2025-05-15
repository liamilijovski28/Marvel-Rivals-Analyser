from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField, PasswordField, StringField, SelectField
from wtforms.validators import DataRequired, Length, Optional

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
    new_username = StringField("New Username", validators=[Optional(), Length(min=3, max=80)])
    new_password = PasswordField("New Password", validators=[Optional(), Length(min=8)])
    new_playerID = StringField("New Player ID", validators=[Optional(), Length(9)])
    data_sharing = SelectField("Share my data with friends", choices=[("yes", "Yes"), ("no", "No")])
    restricted_friends = StringField("Restricted Friends", validators=[Optional()])
    
    submit = SubmitField("Save Changes")
    logout = SubmitField("Logout")
    close_account = SubmitField("Close Account")
