@app.route('/loans/update_status/<int:loan_id>', methods=['POST'])
@login_required
def update_loan_status(loan_id):
    loan = Loan.query.get(loan_id)

    if loan:
        # Calculate remaining balance and check overdue
        if loan.balance <= 0:
            loan.status = 'completed'
        elif loan.due_date < datetime.utcnow():
            loan.status = 'overdue'
            apply_penalty(loan)

        db.session.commit()
        flash(f"Loan status updated to {loan.status}.", "success")
    return redirect(url_for('loan_dashboard'))
