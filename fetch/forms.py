from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, min_length

class LoginForm(FlaskForm):
    username = StringField('Student ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), min_length(8)])
    submit = SubmitField('Sign in')