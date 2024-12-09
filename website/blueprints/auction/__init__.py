from flask import Blueprint

bp = Blueprint('auction', __name__, template_folder='templates')

from blueprints.auction import routes
