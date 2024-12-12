from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from blueprints.bank import bp
from utils import db, User, Loan, Transaction, Savings


# Dashboard Route
@bp.route('/', methods=['GET'])
@login_required
def index():
    """Bank dashboard with transaction history and pagination."""
    page = request.args.get('page', 1, type=int)  # Get the current page number from query params
    per_page = 10  # Number of transactions per page

    # Fetch the current user's transactions
    pagination = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return render_template(
        'bank_index.html',
        user=current_user,
        transactions=pagination.items,
        pagination=pagination
    )


@bp.route('/savings', methods=['GET'])
@login_required
def view_savings():
    """View savings account details and transaction history with pagination."""
    page = request.args.get('page', 1, type=int)  # Get the current page number from query params
    per_page = 10  # Number of transactions per page

    # Fetch the savings account for the current user
    savings = Savings.query.filter_by(user_id=current_user.id).first()

    if not savings:
        savings = Savings(user_id=current_user.id, amount=0, goal=0)
        db.session.add(savings)
        db.session.commit()

    # Fetch the transaction history for savings-related actions
    pagination = Transaction.query.filter_by(user_id=current_user.id, action='savings').order_by(
        Transaction.timestamp.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'savings_dashboard.html',
        account=savings,
        transactions=pagination.items,
        pagination=pagination
    )


@bp.route('/savings/setgoal', methods=['POST'])
@login_required
def set_goal():
    """Set a savings goal."""
    goal = request.form.get('goal', type=float)  # Fetch from form data instead of args

    # Validate the input
    if goal is None or goal <= 0:
        flash('Goal must be a positive value.', 'danger')
        return redirect(url_for('bank.view_savings'))

    # Retrieve or create the savings account
    savings = Savings.query.filter_by(user_id=current_user.id).first()
    if not savings:
        savings = Savings(user_id=current_user.id, amount=0, goal=goal)
        db.session.add(savings)
    else:
        savings.goal = goal

    db.session.commit()
    flash(f'Savings goal set to ${goal:.2f}', 'success')
    return redirect(url_for('bank.view_savings'))


@bp.route('/savings/transaction', methods=['POST'])
@login_required
def handle_transaction():
    """Handle savings transactions (deposit or withdraw)."""
    amount = request.form.get('amount', type=float)
    action = request.form.get('action')  # 'deposit' or 'withdraw'

    # Validate input
    if amount is None or amount <= 0:
        flash('Amount must be a positive value.', 'danger')
        return redirect(url_for('bank.view_savings'))

    savings = Savings.query.filter_by(user_id=current_user.id).first()

    if not savings:
        flash('Savings account not found.', 'danger')
        return redirect(url_for('bank.view_savings'))

    if action == 'deposit':
        # Handle deposit
        if current_user.balance < amount:
            flash('Insufficient funds in your account.', 'danger')
            return redirect(url_for('bank.view_savings'))

        current_user.balance -= amount
        savings.amount += amount
        transaction_type = 'deposit'
        flash(f'Deposited ${amount:.2f} to savings.', 'success')

    elif action == 'withdraw':
        # Handle withdrawal
        if savings.amount < amount:
            flash('Insufficient funds in savings.', 'danger')
            return redirect(url_for('bank.view_savings'))

        current_user.balance += amount
        savings.amount -= amount
        transaction_type = 'withdraw'
        flash(f'Withdrew ${amount:.2f} from savings.', 'success')

    else:
        flash('Invalid transaction action.', 'danger')
        return redirect(url_for('bank.view_savings'))

    # Log the transaction
    transaction = Transaction(
        user_id=current_user.id,
        amount=amount,
        type=transaction_type,
        action="savings",
        recipient_id=savings.user_id,
    )
    db.session.add(transaction)
    db.session.commit()

    return redirect(url_for('bank.view_savings'))


@bp.route('/transfer', methods=['POST'])
@login_required
def transfer_funds():
    """Handle transferring funds between users."""
    recipient_username = request.form.get('recipient_username', type=str)
    amount = request.form.get('amount', type=float)

    # Validate input
    if not recipient_username:
        flash(f'Invalid recipient {recipient_username}.', 'danger')
        return redirect(url_for('bank.index'))

    # Validate amount
    if not amount or amount <= 0:
        flash('Invalid amount.', 'danger')
        return redirect(url_for('bank.index'))

    if current_user.username == recipient_username:
        flash('You cannot transfer funds to yourself.', 'danger')
        return redirect(url_for('bank.index'))

    # Check user balance
    if current_user.balance < amount:
        flash('Insufficient balance.', 'danger')
        return redirect(url_for('bank.index'))

    # Find the recipient
    recipient = User.query.filter_by(username=recipient_username).first()
    if not recipient:
        flash('Recipient not found.', 'danger')
        return redirect(url_for('bank.index'))

    # Perform the transfer
    current_user.balance -= amount
    current_user.net_worth -= amount
    recipient.balance += amount
    recipient.net_worth += amount

    # Log the transaction
    transaction = Transaction(
        user_id=current_user.id,
        amount=amount,
        type='transfer',
        action='outgoing',
        recipient_id=recipient.id,
        timestamp=datetime.utcnow()
    )
    db.session.add(transaction)

    transaction_recipient = Transaction(
        user_id=recipient.id,
        amount=amount,
        type='transfer',
        action='incoming',
        sender_id=current_user.id,
        timestamp=datetime.utcnow()
    )
    db.session.add(transaction_recipient)

    db.session.commit()
    flash(f'Successfully transferred ${amount:.2f} to User ID {recipient_username}.', 'success')
    return redirect(url_for('bank.index'))


# Credit score to interest rate mapping
def get_interest_rate(credit_score):
    if credit_score >= 750:
        return 3.5
    elif 700 <= credit_score < 750:
        return 4.5
    elif 650 <= credit_score < 700:
        return 6.0
    else:
        return 8.5


def calculate_max_loan(credit_score, net_worth) -> float:
    # Base loan factor based on credit score
    if credit_score >= 750:
        base_factor = 1.00
    elif credit_score >= 650:
        base_factor = 0.70
    else:
        base_factor = 0.50

    return net_worth * base_factor


@bp.route('/loans', methods=['GET', 'POST'])
@login_required
def loan_dashboard():
    """Loan dashboard with loan details and application form."""
    # Fetch the user's active loan (if any)
    loan = Loan.query.filter_by(user_id=current_user.id, status='active').first()

    user = User.query.filter_by(id=current_user.id).first()
    max_loan = round(calculate_max_loan(user.credit_score, user.net_worth))

    return render_template('loan_dashboard.html', loan=loan, max_loan=max_loan)


@bp.route('/apply-loan', methods=['POST'])
@login_required
def apply_loan():
    """Apply for a new loan."""
    amount = request.form.get('amount', type=float)
    term = request.form.get('term', type=int)

    if not amount or not term or amount <= 0 or term <= 0:
        flash('Invalid loan amount or term.', 'danger')
        return redirect(url_for('bank.loan_dashboard'))

    if Loan.query.filter_by(user_id=current_user.id, status='active').first():
        flash('You already have an active loan.', 'danger')
        return redirect(url_for('bank.loan_dashboard'))

    # Determine interest rate based on credit score
    interest_rate = get_interest_rate(current_user.credit_score)

    # Calculate monthly payment using the formula:
    # M = P * (r(1 + r)^n) / ((1 + r)^n - 1)
    # Where:
    # P = loan amount
    # r = monthly interest rate (annual rate / 12)
    # n = number of payments (term in months)

    monthly_rate = interest_rate / 100 / 12
    monthly_payment = amount * (monthly_rate * (1 + monthly_rate) ** term) / ((1 + monthly_rate) ** term - 1)
    max_loan = calculate_max_loan(current_user.credit_score, current_user.net_worth)

    if amount > max_loan:
        flash(f'Your max loan is {max_loan}', 'danger')
        return redirect(url_for('bank.loan_dashboard'))

    # Create a new loan
    loan = Loan(
        user_id=current_user.id,
        amount=amount,
        interest_rate=interest_rate,
        term=term,
        monthly_payment=monthly_payment,
        remaining_balance=amount,
        next_payment_due=datetime.utcnow() + timedelta(days=2),
        status='active'
    )

    payment_transaction = Transaction(
        user_id=current_user.id,
        amount=amount,
        type='loan',
        action='incoming',
        sender_id=1,
        timestamp=datetime.utcnow()
    )
    db.session.add(payment_transaction)

    user = User.query.filter_by(username=current_user.username).first()
    user.balance += amount

    db.session.add(loan)
    db.session.commit()

    flash(f'Loan approved! Your monthly payment is ${monthly_payment:.2f}', 'success')
    return redirect(url_for('bank.loan_dashboard'))


@bp.route('/make-payment', methods=['POST'])
@login_required
def make_payment():
    """Handle loan payments."""
    payment_amount = request.form.get('payment_amount', type=float)

    if not payment_amount or payment_amount <= 0:
        flash('Invalid payment amount.', 'danger')
        return redirect(url_for('bank.loan_dashboard'))

    # Fetch the user's active loan
    loan = Loan.query.filter_by(user_id=current_user.id, status='active').first()

    if not loan:
        flash('You do not have an active loan.', 'danger')
        return redirect(url_for('bank.loan_dashboard'))

    # Ensure the user has sufficient balance
    if current_user.balance < payment_amount:
        flash('Insufficient balance to make this payment.', 'info')
        return redirect(url_for('bank.loan_dashboard'))

    # Ensure the user is knows that they are only paying the max
    if payment_amount > loan.remaining_balance:
        flash(f'You attempted to overpay. {loan.remaining_balance:.2f} has been payed out', 'danger')
        payment_amount = loan.remaining_balance

    # Deduct the payment from the user's balance
    current_user.balance -= payment_amount
    current_user.credit_score += 5

    # Apply the payment to the loan
    loan.remaining_balance -= payment_amount
    if loan.remaining_balance <= 0:
        loan.remaining_balance = 0
        loan.status = 'paid'
        flash('Congratulations! Your loan has been fully repaid.', 'success')
    else:
        flash(f'Payment of ${payment_amount:.2f} applied to your loan.', 'success')

    # Record the payment as a transaction
    payment_transaction = Transaction(
        user_id=current_user.id,
        amount=payment_amount,
        type='loan',
        action='outgoing',
        recipient_id=1,
        timestamp=datetime.utcnow()
    )
    db.session.add(payment_transaction)
    db.session.commit()

    return redirect(url_for('bank.loan_dashboard'))
