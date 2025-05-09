from flask import Flask
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
app.secret_key = 'change this later'
csrf = CSRFProtect(app)
from fetch import routes