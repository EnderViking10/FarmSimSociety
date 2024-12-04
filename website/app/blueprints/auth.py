from database import User
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    """Login page for user authentication."""
    session_local = current_app.config['SESSION_LOCAL']
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = None
        with session_local() as session:
            user = session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password!', 'danger')

    return render_template('index.html')
