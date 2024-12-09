from datetime import datetime, timedelta

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from blueprints.auction import bp
from utils import Auction, Properties, db


@bp.route('/', methods=['GET'])
@login_required
def index():
    auctions = Auction.query.all()
    return render_template('auction.html', auctions=auctions)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_auction():
    if request.method == 'POST':
        property_id = request.form.get('property_id')
        starting_bid = request.form.get('starting_bid', type=int)

        # Validate the inputs
        if not property_id or not starting_bid:
            flash("All fields are required.", "danger")
            return redirect(url_for('auction.create_auction'))

        try:
            auction_property = Properties.query.get(property_id)
            if not auction_property:
                flash("Invalid property selected.", "danger")
                return redirect(url_for('auction.create_auction'))

            # Create a new auction
            auction = Auction(
                property_id=property_id,
                server_id=auction_property.server_id,
                cost=starting_bid,
                timeout=datetime.utcnow() + timedelta(hours=24)
            )
            db.session.add(auction)
            db.session.commit()
            flash("Auction created successfully!", "success")
            return redirect(url_for('auction.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating auction: {e}", "danger")
            return redirect(url_for('auction.create_auction'))

    # Fetch properties for dropdown
    properties = Properties.query.all()
    return render_template('create_auction.html', properties=properties)


@bp.route('/<int:auction_id>/bid', methods=['POST'])
@login_required
def place_bid(auction_id):
    auction = Auction.query.get_or_404(auction_id)

    # Ensure the user is not the owner of the property
    if auction.property.owner and auction.property.owner.id == current_user.id:
        flash("You cannot bid on your own auction.", "danger")
        return redirect(url_for('auction.index'))

    # Ensure the auction is still active
    if auction.timeout < datetime.utcnow():
        flash("This auction has already ended.", "danger")
        return redirect(url_for('auction.index'))

    # Update the highest bid
    try:
        auction.cost += 5000  # Increment by 5000
        auction.highest_bidder = current_user.id
        db.session.commit()
        flash("Your bid was successfully placed!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "danger")

    return redirect(url_for('auction.index'))
