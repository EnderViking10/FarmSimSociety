@app.route('/loans/apply', methods=['POST'])
@login_required
def apply_loan():
    principal = float(request.form.get('principal'))
    credit_score = current_user.credit_score  # Get the current user's credit score
    interest_rate = get_dynamic_interest_rate(principal, credit_score)  # Get the dynamic interest rate

    loan = Loan(
        user_id=current_user.id,
        principal=principal,
        interest_rate=interest_rate,
        term_years=int(request.form.get('term_years')),
        compounding_frequency=int(request.form.get('compounding_frequency')),
        balance=principal * (1 + interest_rate / 12) ** 12,  # Calculate compound interest
        due_date=datetime.utcnow() + timedelta(days=30)  # First payment due in 30 days
    )
    db.session.add(loan)
    db.session.commit()

    flash("Loan application submitted successfully!", "success")
    return redirect(url_for('loan_dashboard'))
