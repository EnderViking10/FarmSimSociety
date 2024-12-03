import sqlite3
from getpass import getpass

from flask import Flask
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management


@app.cli.command('initdb')
def initdb():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")


# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL, 
            balance REAL DEFAULT 0
        )
    ''')

    # Transactions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Admin Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Create default admin
    cursor.execute("INSERT OR IGNORE INTO admin (id, username, password) VALUES (1, 'admin', 'password')")
    conn.commit()
    conn.close()


# CLI command to create an admin user
@app.cli.command('createadmin')
def createadmin():
    """Create an admin user."""
    username = input("Enter admin username: ")
    password = getpass("Enter admin password: ")
    if User.query.filter_by(username=username).first():
        print("Admin with this username already exists!")
        return
    admin = User(username=username, password=generate_password_hash(password), is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user '{username}' created!")


def main():
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])


if __name__ == '__main__':
    main()
