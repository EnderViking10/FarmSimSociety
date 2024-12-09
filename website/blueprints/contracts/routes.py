from datetime import datetime

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app import db
from blueprints.contracts import bp
from blueprints.contracts.forms import ContractForm
from utils import Contracts, Server


@bp.route('/', methods=['GET'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    contracts = Contracts.query.filter_by(status='open').paginate(page=page, per_page=10)
    return render_template('contracts.html', contracts=contracts)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_contract():
    form = ContractForm()

    # Fetch servers for the dropdown
    servers = Server.query.all()
    form.server_id.choices = [(server.id, server.name) for server in servers]

    if form.validate_on_submit():
        try:
            new_contract = Contracts(
                user_id=current_user.id,
                server_id=form.server_id.data,
                title=form.title.data,
                description=form.description.data,
                status="open",
                price=form.price.data,
                type=form.type.data,
            )
            db.session.add(new_contract)
            db.session.commit()
            flash('Contract created successfully!', 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error creating contract: {str(e)}", 'danger')

        return redirect(url_for('contracts.index'))

    return render_template('create_contract.html', form=form)


@bp.route('/<int:contract_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contract(contract_id):
    contract = Contracts.query.get_or_404(contract_id)

    # Ensure the user owns the contract
    if contract.user_id != current_user.id:
        flash("Unauthorized to edit this contract.", "danger")
        return redirect(url_for('contracts.contracts'))

    form = ContractForm(obj=contract)
    servers = Server.query.all()
    form.server_id.choices = [(server.id, server.name) for server in servers]
    
    if form.validate_on_submit():
        try:
            contract.title = form.title.data
            contract.description = form.description.data
            contract.server_id = form.server_id.data
            contract.price = form.price.data
            contract.type = form.type.data
            db.session.commit()
            flash('Contract updated successfully!', 'success')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error updating contract: {str(e)}", 'danger')
        return redirect(url_for('contracts.index'))

    return render_template('edit_contract.html', form=form, contract=contract)


@bp.route('/<int:contract_id>/delete', methods=['POST'])
@login_required
def delete_contract(contract_id):
    contract = Contracts.query.get_or_404(contract_id)

    # Ensure the user owns the contract
    if contract.user_id != current_user.id:
        flash("Unauthorized to delete this contract.", "danger")
        return redirect(url_for('contracts.index'))

    try:
        db.session.delete(contract)
        db.session.commit()
        flash('Contract deleted successfully!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error deleting contract: {str(e)}", 'danger')

    return redirect(url_for('contracts.index'))


@bp.route('/<int:contract_id>/accept', methods=['POST'])
@login_required
def accept_contract(contract_id):
    contract = Contracts.query.get_or_404(contract_id)

    if not contract:
        flash("Contract not found.", "danger")
        return redirect(url_for('contracts.index'))

    # Ensure the current user is not the owner of the contract
    if contract.user_id == current_user.id:
        flash("You cannot accept your own contract.", "danger")
        return redirect(url_for('contracts.index'))

    # Check if the contract is already accepted
    if contract.status == 'accepted':
        flash("This contract has already been accepted.", "warning")
        return redirect(url_for('contracts.index'))

    try:
        contract.status = 'accepted'
        contract.contractor_id = current_user.id
        contract.start_time = datetime.utcnow()
        db.session.commit()
        flash('Contract accepted successfully!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error accepting contract: {str(e)}", 'danger')

    return redirect(url_for('contracts.index'))


@bp.route('/<int:contract_id>/complete', methods=['POST'])
@login_required
def complete_contract(contract_id):
    contract = Contracts.query.get_or_404(contract_id)

    # Ensure the user is either the owner or the contractor
    if contract.user_id != current_user.id and contract.contractor_id != current_user.id:
        flash("Unauthorized to complete this contract.", "danger")
        return redirect(url_for('contracts.index'))

    if contract.status != "accepted":
        flash("Only accepted contracts can be completed.", "warning")
        return redirect(url_for('contracts.index'))

    try:
        contract.status = "completed"
        contract.end_time = datetime.utcnow()
        db.session.commit()
        flash('Contract marked as completed!', 'success')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error completing contract: {str(e)}", 'danger')

    return redirect(url_for('contracts.index'))


@bp.route('/open', methods=['GET'])
@login_required
def open_contracts():
    page = request.args.get('page', 1, type=int)
    contracts = Contracts.query.filter_by(status='open').paginate(page=page, per_page=10)
    return render_template('contracts_open.html', contracts=contracts)


@bp.route('/accepted', methods=['GET'])
@login_required
def accepted_contracts():
    page = request.args.get('page', 1, type=int)
    # Show only contracts where the current user is the contractor
    contracts = Contracts.query.filter(
        (Contracts.status == "accepted") &
        (Contracts.contractor_id == current_user.id)
    ).paginate(page=page, per_page=10)
    return render_template('contracts_accepted.html', contracts=contracts)


@bp.route('/completed', methods=['GET'])
@login_required
def completed_contracts():
    page = request.args.get('page', 1, type=int)
    # Show only contracts where the current user is the contractor
    contracts = Contracts.query.filter(
        (Contracts.status == "completed") &
        (Contracts.contractor_id == current_user.id)
    ).paginate(page=page, per_page=10)
    return render_template('contracts_completed.html', contracts=contracts)
