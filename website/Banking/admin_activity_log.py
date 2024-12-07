@app.route('/admin/activity-log')
@login_required
def admin_activity_log():
    if not current_user.is_admin:
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for('index'))

    logs = AdminActivityLog.query.order_by(AdminActivityLog.timestamp.desc()).all()
    return render_template('admin_activity_log.html', logs=logs)
