from flask import Blueprint

bp = Blueprint('bank', __name__, template_folder='templates')

from blueprints.bank import routes
