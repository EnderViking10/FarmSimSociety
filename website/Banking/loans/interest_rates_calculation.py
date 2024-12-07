@app.route('/loans/apply', methods=['POST'])
@login_required
def apply_loan():
    principal = float(request.form.get('principal'))
    credit_score = current_user.credit_score  # User's credit score
    interest_rate = get_dynamic_interest_rate(principal, credit_score)  # Calculate dynamic rate

    loan = Loan(
        user_id=current_user.id,
        principal=principal,
        interest_rate=interest_rate,
        term_years=int(request.form.get('term_years')),
        compounding_frequency=int(request.form.get('compounding_frequency')),
        balance=principal * (1 + interest_rate / 12) ** 12,  # Example calculation
        due_date=datetime.utcnow() + timedelta(days=30)
    )
    db.session.add(loan)
    db.session.commit()

    flash("Loan application submitted successfully!", "success")
    return redirect(url_for('loan_dashboard'))

def get_dynamic_interest_rate(principal, credit_score):
    if credit_score > 750:
        rate = 0.05  # 5% interest for good credit score
    elif credit_score > 650:
        rate = 0.08  # 8% interest for average credit score
    else:
        rate = 0.12  # 12% interest for low credit score

    if principal > 10000:
        rate += 0.02  # 2% higher interest for large loans

    return rate
