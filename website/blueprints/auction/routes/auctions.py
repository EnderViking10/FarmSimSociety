from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import Auction, Bid, db

auction_bp = Blueprint("auction", __name__, url_prefix="/auction")

# Create New Auction
@auction_bp.route("/create", methods=["POST"])
def create_auction():
    data = request.json
    item_id = data.get("itemID")
    item_name = data.get("itemName")
    seller_id = data.get("sellerID")
    starting_price = data.get("startingPrice")
    duration = data.get("duration")  # Duration in minutes

    try:
        end_time = datetime.utcnow() + timedelta(minutes=duration)

        auction = Auction(
            item_id=item_id,
            item_name=item_name,
            seller_id=seller_id,
            starting_price=starting_price,
            current_bid=starting_price,
            end_time=end_time,
        )
        db.session.add(auction)
        db.session.commit()

        return jsonify({"message": "Auction created successfully", "auction": auction.to_dict()}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Place a Bid
@auction_bp.route("/bid", methods=["POST"])
def place_bid():
    data = request.json
    auction_id = data.get("auctionID")
    bidder_id = data.get("bidderID")
    amount = data.get("amount")

    try:
        auction = Auction.query.get(auction_id)

        if not auction or auction.status != "active":
            return jsonify({"message": "Auction not found or already completed"}), 404

        if amount <= auction.current_bid:
            return jsonify({"message": "Bid must be higher than the current bid"}), 400

        # Update auction with new bid
        auction.current_bid = amount
        auction.current_bidder_id = bidder_id
        db.session.commit()

        # Log the bid
        bid = Bid(auction_id=auction_id, bidder_id=bidder_id, amount=amount)
        db.session.add(bid)
        db.session.commit()

        return jsonify({"message": "Bid placed successfully", "auction": auction.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get Active Auctions
@auction_bp.route("/active", methods=["GET"])
def get_active_auctions():
    try:
        active_auctions = Auction.query.filter_by(status="active").all()
        return jsonify([auction.to_dict() for auction in active_auctions]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Complete Auctions
@auction_bp.route("/complete", methods=["POST"])
def complete_auction():
    data = request.json
    auction_id = data.get("auctionID")

    try:
        auction = Auction.query.get(auction_id)

        if not auction or auction.status != "active":
            return jsonify({"message": "Auction not found or already completed"}), 404

        auction.status = "completed"
        db.session.commit()

        return jsonify({"message": "Auction completed successfully", "auction": auction.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
