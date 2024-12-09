from flask import render_template

from blueprints.main import bp


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/rules', methods=['GET'])
def rules():
    return render_template('rules.html')
