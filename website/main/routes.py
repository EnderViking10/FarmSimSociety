from database import ContractRepository, UserRepository
from flask import render_template
from main import bp

from app import session

@bp.route('/')
@bp.route('/index')
def index():
    print("aa")
    return render_template('index.html')


@bp.route('/rules', methods=['GET'])
def rules():
    return render_template('rules.html')


@bp.route('/contracts', methods=['GET'])
def contracts_page():
    contracts = ContractRepository.get_all_contracts(session)

    return render_template('contracts.html', contracts=contracts)