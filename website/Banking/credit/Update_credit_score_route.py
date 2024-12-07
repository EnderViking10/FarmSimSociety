@app.route('/update_credit_score', methods=['POST'])
@login_required
def update_credit_score():
    new_credit_score = int(request.form.get('credit_score'))
    
    # Validate credit score (between 300 and 850)
    if 300 <= new_credit_score <= 850:
        current_user.credit_score = new_credit_score
        db.session.commit()
        flash('Credit score updated successfully!', 'success')
    else:
        flash('Invalid credit score. Please enter a value between 300 and 850.', 'danger')

    return redirect(url_for('profile'))
