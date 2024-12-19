from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Bid(db.Model):
    __tablename__ = "bids"

    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'), nullable=False)  # ForeignKey to Auction
    bidder_id = db.Column(db.String(255), nullable=False)  # bidderID in Mongoose
    amount = db.Column(db.Float, nullable=False)  # amount in Mongoose
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # timestamp in Mongoose

    auction = db.relationship("Auction", backref="bids")  # Define relationship to Auction

    def __repr__(self):
        return f"<Bid {self.amount} on Auction {self.auction_id} by {self.bidder_id}>"
