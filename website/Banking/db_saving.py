from datetime import datetime
from app import db

class SavingsAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Float, default=0.0, nullable=False)
    goal = db.Column(db.Float, default=0.0, nullable=True)  # Savings goal
    interest_rate = db.Column(db.Float, default=0.02, nullable=False)  # Annual interest rate
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    transactions = db.relationship('SavingsTransaction', backref='account', lazy=True)
