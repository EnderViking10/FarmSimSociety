@main.route('/savings', methods=['GET', 'POST'])
@login_required
def savings_dashboard():
    account = SavingsAccount.query.filter_by(user_id=current_user.id).first()
    if not account:
        account = SavingsAccount(user_id=current_user.id, balance=0.0)
        db.session.add(account)
        db.session.commit()

    transactions = SavingsTransaction.query.filter_by(account_id=account.id).order_by(SavingsTransaction.timestamp.desc()).all()

    if request.method == 'POST':
        # Handle setting savings goal
        goal = float(request.form['goal'])
        if goal <= 0:
            flash("Savings goal must be greater than zero.", "danger")
        else:
            account.goal = goal
            db.session.commit()
            flash(f"Savings goal set to ${goal:.2f}.", "success")
        return redirect(url_for('savings_dashboard'))

    return render_template('savings_dashboard.html', account=account, transactions=transactions)
