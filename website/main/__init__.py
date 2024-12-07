from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='templates')


def route():
    return None