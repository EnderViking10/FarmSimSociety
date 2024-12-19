from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)  # ForeignKey to Admin
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    details = db.Column(db.JSON)  # This will allow storing a JSON object for details

    admin = db.relationship("Admin", backref="logs")  # Define relationship to Admin

    def __repr__(self):
        return f"<Log {self.action} by Admin {self.admin_id} at {self.timestamp}>"
