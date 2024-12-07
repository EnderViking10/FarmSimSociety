class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)  # APC as a decimal
    term_years = db.Column(db.Integer, nullable=False)
    compounding_frequency = db.Column(db.Integer, default=12)  # Monthly, quarterly, etc.
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    balance = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="active")  # active, completed, overdue
    last_payment_date = db.Column(db.DateTime)
    penalty = db.Column(db.Float, default=0.0)  # Penalties for late payment
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_score = db.Column(db.Integer, default=700)  # User's credit score
