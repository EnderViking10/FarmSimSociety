@app.route('/admin/manage_credit_score/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def manage_credit_score(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        new_credit_score = int(request.form.get('credit_score'))
        
        if 300 <= new_credit_score <= 850:
            user.credit_score = new_credit_score
            db.session.commit()
            flash('Credit score updated successfully!', 'success')
        else:
            flash('Invalid credit score. Please enter a value between 300 and 850.', 'danger')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/manage_credit_score.html', user=user)
