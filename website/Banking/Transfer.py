@app.route('/savings/transfer', methods=['POST'])
@login_required
def savings_transfer():
    account = SavingsAccount.query.filter_by(user_id=current_user.id).first()
    recipient_id = request.form['recipient_id']
    amount = float(request.form['amount'])

    if amount <= 0 or amount > account.balance:
        flash("Invalid transfer amount.", "danger")
        return redirect(url_for('savings_dashboard'))

    recipient = SavingsAccount.query.filter_by(user_id=recipient_id).first()
    if not recipient:
        flash("Recipient savings account not found.", "danger")
        return redirect(url_for('savings_dashboard'))

    # Perform transfer
    account.balance -= amount
    recipient.balance += amount
    db.session.add(SavingsTransaction(account_id=account.id, action='transfer', amount=-amount))
    db.session.add(SavingsTransaction(account_id=recipient.id, action='transfer', amount=amount))
    db.session.commit()

    flash(f"Transferred ${amount:.2f} to user {recipient_id}.", "success")
    return redirect(url_for('savings_dashboard'))
