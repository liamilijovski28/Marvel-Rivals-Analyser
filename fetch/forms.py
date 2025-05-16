from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign in')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=25),
        Regexp(r'^[A-Za-z0-9_]+$', message="Username must be alphanumeric")
    ])

    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters"),
        Regexp(r'(?=.*[A-Z])', message="Must contain an uppercase letter"),
        Regexp(r'(?=.*\d)', message="Must contain a digit"),
        Regexp(r'(?=.*[!@#$%^&*])', message="Must contain a special character")
    ])

    player_id = StringField('Player ID', validators=[
        DataRequired(message="Player ID is required"),
        Regexp(r'^\d+$', message="Player ID must be numeric")
    ])

    submit = SubmitField('Sign up')


class SettingsForm(FlaskForm):
    new_username = StringField("New Username", validators=[Optional(), Length(min=3, max=80)])
    new_password = PasswordField("New Password", validators=[Optional(), Length(min=8)])
    new_playerID = StringField("New Player ID", validators=[Optional(), Length(min=9, max=9)])
    data_sharing = SelectField("Share my data with friends", choices=[("yes", "Yes"), ("no", "No")])
    restricted_friends = StringField("Restricted Friends", validators=[Optional()])

    submit = SubmitField("Save Changes")
    logout = SubmitField("Logout")
    close_account = SubmitField("Close Account")
