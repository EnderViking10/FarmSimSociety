@app.route('/savings/transaction', methods=['POST'])
@login_required
def savings_transaction():
    account = SavingsAccount.query.filter_by(user_id=current_user.id).first()
    if not account:
        flash("No savings account found.", "danger")
        return redirect(url_for('savings_dashboard'))

    action = request.form['action']
    amount = float(request.form['amount'])

    if amount <= 0:
        flash("Amount must be greater than zero.", "danger")
        return redirect(url_for('savings_dashboard'))

    if action == 'deposit':
        account.balance += amount
        db.session.add(SavingsTransaction(account_id=account.id, action='deposit', amount=amount))
        flash(f"Deposited ${amount:.2f} to savings.", "success")
    elif action == 'withdraw':
        if amount > account.balance:
            flash("Insufficient funds for withdrawal.", "danger")
        else:
            account.balance -= amount
            db.session.add(SavingsTransaction(account_id=account.id, action='withdraw', amount=-amount))
            flash(f"Withdrew ${amount:.2f} from savings.", "success")
    else:
        flash("Invalid transaction type.", "danger")

    db.session.commit()
    return redirect(url_for('savings_dashboard'))
