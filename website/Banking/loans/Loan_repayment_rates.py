@app.route('/loans/repay/<int:loan_id>', methods=['POST'])
@login_required
def repay_loan(loan_id):
    loan = Loan.query.get(loan_id)

    if loan:
        repayment_amount = float(request.form.get('repayment_amount'))

        if repayment_amount >= loan.balance:
            loan.balance = 0
            loan.status = 'completed'
        else:
            loan.balance -= repayment_amount

        loan.interest_rate = adjust_rate_based_on_market(loan.principal, current_user.credit_score)

        db.session.commit()
        flash(f"Payment of ${repayment_amount} successful.", "success")
    return redirect(url_for('loan_dashboard'))
