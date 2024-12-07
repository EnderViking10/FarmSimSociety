from datetime import datetime
from app import db

class AdminActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Admin who performed the action
    action = db.Column(db.String(255), nullable=False)  # Description of the action
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
