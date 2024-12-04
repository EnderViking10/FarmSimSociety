import sqlite3

from flask import Blueprint, request, session, redirect, url_for, render_template
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid credentials"

    return render_template('admin_login.html')


@main.route('/admin/dashboard')
#@login_required
def admin_dashboard():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch all users
    #cursor.execute("SELECT id, username, balance FROM users")
    users = cursor.fetchall()

    # Fetch recent transactions
    #cursor.execute("SELECT t.id, u.username, t.type, t.amount, t.timestamp FROM transactions t "
                   "JOIN users u ON t.user_id = u.id ORDER BY t.timestamp DESC LIMIT 10")
    transactions = cursor.fetchall()

    conn.close()

    return render_template('admin_dashboard.html', users=users, transactions=transactions)


@main.route('/admin/logout')
#@login_required
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))


@main.route('/admin/edit_balance', methods=['POST'])
#@login_required
def edit_balance():
    user_id = request.form['user_id']
    new_balance = float(request.form['new_balance'])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))


@main.route('/admin/add_user', methods=['POST'])
#@login_required
def add_user():
    username = request.form['username']
    balance = float(request.form['balance'])

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #cursor.execute("INSERT INTO users (username, balance) VALUES (?, ?)", (username, balance))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))


@main.route('/admin/delete_user', methods=['POST'])
#@login_required
def delete_user():
    user_id = request.form['user_id']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    #cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))
