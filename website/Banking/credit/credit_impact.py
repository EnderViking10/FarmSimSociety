@app.route('/admin/approve_loan/<int:loan_id>', methods=['POST'])
@admin_required
def approve_loan(loan_id):
    loan = Loan.query.get(loan_id)
    
    if loan:
        if current_user.credit_score < 600:  # Deny loans for users with low credit scores
            flash("Loan cannot be approved due to low credit score,see admin for assisant.", "danger")
            loan.status = "rejected"
        else:
            loan.status = "approved"
            flash("Loan approved successfully!", "success")
        
        db.session.commit()
    return redirect(url_for('admin_dashboard'))
