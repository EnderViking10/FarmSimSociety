@app.route('/admin/savings/<int:account_id>/transactions')
@login_required
def admin_transaction_history(account_id):
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('index'))

    account = SavingsAccount.query.get(account_id)
    if not account:
        flash("Account not found.", "danger")
        return redirect(url_for('admin_savings'))

    transactions = SavingsTransaction.query.filter_by(account_id=account_id).order_by(SavingsTransaction.timestamp.desc()).all()
    return render_template('admin_transactions.html', account=account, transactions=transactions)
