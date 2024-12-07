class SavingsTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('savings_account.id'), nullable=False)
    action = db.Column(db.String(10), nullable=False)  # "deposit", "withdraw", "interest", "transfer"
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
