from flask import render_template
from main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@bp.route('/rules', methods=['GET', 'POST'])
def rules():
    return render_template('rules.html')
