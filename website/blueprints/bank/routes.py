from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from utils import db, User, Loan, Transaction

app = Flask(__name__)


# Dashboard Route
@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    loans = Loan.query.filter_by(user_id=current_user.id).all()
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(10)
    return render_template(
        'dashboard.html',
        user=current_user,
        loans=loans,
        transactions=transactions
    )


# Savings Management Routes
@bp.route('/savings/transaction', methods=['POST'])
@login_required
def savings_transaction():
    amount = float(request.form.get('amount'))
    transaction_type = request.form.get('type')  # "deposit" or "withdraw"

    if transaction_type == "withdraw" and current_user.balance < amount:
        flash("Insufficient balance for withdrawal.", "danger")
    else:
        if transaction_type == "withdraw":
            current_user.balance -= amount
        else:
            current_user.balance += amount
        # Log transaction
        transaction = Transaction(
            user_id=current_user.id,
            amount=amount,
            type=transaction_type,
            timestamp=datetime.utcnow()
        )
        db.session.add(transaction)
        db.session.commit()
        flash(f"{transaction_type.capitalize()} of ${amount} successful!", "success")
    return redirect(url_for('dashboard'))


@bp.route('/savings/transfer', methods=['POST'])
@login_required
def savings_transfer():
    recipient_id = int(request.form.get('recipient_id'))
    amount = float(request.form.get('amount'))
    recipient = User.query.get(recipient_id)

    if recipient and current_user.balance >= amount:
        current_user.balance -= amount
        recipient.balance += amount
        # Log transactions
        transaction = Transaction(
            user_id=current_user.id,
            amount=amount,
            type="transfer-out",
            recipient_id=recipient_id,
            timestamp=datetime.utcnow()
        )
        db.session.add(transaction)
        recipient_transaction = Transaction(
            user_id=recipient_id,
            amount=amount,
            type="transfer-in",
            sender_id=current_user.id,
            timestamp=datetime.utcnow()
        )
        db.session.add(recipient_transaction)
        db.session.commit()
        flash(f"Transferred ${amount} to {recipient.username}.", "success")
    else:
        flash("Transfer failed. Check recipient and balance.", "danger")
    return redirect(url_for('dashboard'))


# Loan Management Routes
@bp.route('/loans/apply', methods=['POST'])
@login_required
def apply_loan():
    principal = float(request.form.get('principal'))
    term_years = int(request.form.get('term_years'))
    credit_score = current_user.credit_score

    # Calculate dynamic interest rate (Example logic)
    interest_rate = 0.05 if credit_score > 700 else 0.1
    balance = principal * (1 + interest_rate / 12) ** (12 * term_years)

    loan = Loan(
        user_id=current_user.id,
        principal=principal,
        interest_rate=interest_rate,
        term_years=term_years,
        balance=balance,
        due_date=datetime.utcnow() + timedelta(days=30)
    )
    db.session.add(loan)
    db.session.commit()
    flash("Loan application successful!", "success")
    return redirect(url_for('dashboard'))


@bp.route('/loans/repay/<int:loan_id>', methods=['POST'])
@login_required
def repay_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    amount = float(request.form.get('amount'))

    if amount <= loan.balance:
        loan.balance -= amount
        if loan.balance == 0:
            loan.status = "paid"
        db.session.commit()
        flash("Repayment successful!", "success")
    else:
        flash("Repayment amount exceeds loan balance.", "danger")
    return redirect(url_for('dashboard'))


# Credit Score View
@bp.route('/credit-score', methods=['GET'])
@login_required
def view_credit_score():
    return render_template(
        'credit_score.html',
        credit_score=current_user.credit_score
    )
