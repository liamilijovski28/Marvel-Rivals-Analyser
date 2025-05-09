from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField, PasswordField, StringField
<<<<<<< HEAD
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign in')

class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign up')
=======
from wtforms.validators import DataRequired, min_length

class LoginForm(FlaskForm):
    username = StringField('Student ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), min_length(8)])
    submit = SubmitField('Sign in')
>>>>>>> abeb8ee (created a forms file to handle login and sign ups)
