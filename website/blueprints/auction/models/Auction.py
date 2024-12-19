from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Auction(db.Model):
    __tablename__ = "auctions"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(255), nullable=False)  # itemID in Mongoose
    item_name = db.Column(db.String(255), nullable=False)  # itemName in Mongoose
    seller_id = db.Column(db.String(255), nullable=False)  # sellerID in Mongoose
    starting_price = db.Column(db.Float, nullable=False)  # startingPrice in Mongoose
    current_bid = db.Column(db.Float, default=0.0)  # currentBid in Mongoose
    current_bidder_id = db.Column(db.String(255))  # currentBidderID in Mongoose
    end_time = db.Column(db.DateTime, nullable=False)  # endTime in Mongoose
    status = db.Column(db.String(50), default="active", nullable=False)  # status in Mongoose

    def __repr__(self):
        return f"<Auction {self.item_name} - {self.status}>"
