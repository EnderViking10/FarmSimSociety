from functools import wraps

from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from admin import bp


def admin_required(function):
    @wraps(function)
    def decorated_view(*args, **kwargs):
        if not current_user.admin:
            flash('You must be an admin to see this page')
            return redirect(url_for('main.index'))
        return function(*args, **kwargs)

    return decorated_view


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
@admin_required
def dashboard():
    return render_template("dashboard.html")