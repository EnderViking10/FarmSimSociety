from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import SavingsAccount, SavingsTransaction, AdminActivityLog, User

@app.route('/admin/savings', methods=['GET', 'POST'])
@login_required
def admin_savings():
    # Ensure the user is an admin
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('index'))

    accounts = SavingsAccount.query.all()

    if request.method == 'POST':
        # Handle admin actions (adjust balance, reset goal)
        account_id = request.form['account_id']
        action = request.form['action']
        account = SavingsAccount.query.get(account_id)

        if not account:
            flash("Account not found.", "danger")
            return redirect(url_for('admin_savings'))

        if action == 'adjust_balance':
            new_balance = float(request.form['new_balance'])
            flash(f"Adjusted balance for User {account.user_id} to ${new_balance:.2f}.", "success")
            account.balance = new_balance
            log_action(current_user.id, f"Adjusted balance for User {account.user_id} to ${new_balance:.2f}")
        elif action == 'reset_goal':
            account.goal = None
            flash(f"Reset savings goal for User {account.user_id}.", "success")
            log_action(current_user.id, f"Reset savings goal for User {account.user_id}")
        db.session.commit()

    return render_template('admin_savings.html', accounts=accounts)
