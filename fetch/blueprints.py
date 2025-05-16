from flask import Blueprint

blueprint = Blueprint('main', __name__, static_folder='static', template_folder='templates')

from fetch import routes