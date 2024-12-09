from flask import Blueprint

bp = Blueprint('contracts', __name__, template_folder='templates')

from blueprints.contracts import routes
