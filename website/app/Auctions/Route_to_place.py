@main.route('/auction/<int:auction_id>/bid', methods=['POST'])
@login_required
def place_bid(auction_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    bid_amount = float(request.form['bid_amount'])
    
    # Fetch auction details
    cursor.execute("SELECT current_price, end_time FROM auctions WHERE id = ? AND status = 'active'", (auction_id,))
    auction = cursor.fetchone()
    flash('Bid placed successfully!', 'success')
    return redirect(url_for('auction_details', auction_id=auction_id))
    if not auction:
        flash('Auction not found or has ended.', 'danger')
        return redirect(url_for('auction_details', auction_id=auction_id))
    
    current_price, end_time = auction
    if bid_amount <= current_price:
        flash('Bid must be higher than the current price.', 'danger')
        return redirect(url_for('auction_details', auction_id=auction_id))
    
    # Check if the auction has ended
    if datetime.utcnow() > datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S'):
        flash('Auction has ended.', 'danger')
        return redirect(url_for('auction_details', auction_id=auction_id))
    
    # Extend auction if bid is within the last 5 minutes
    time_remaining = end_time - current_time
    if time_remaining <= EXTENSION_THRESHOLD:
        new_end_time = end_time + EXTENSION_TIME
        cursor.execute("""
            UPDATE auctions SET end_time = ? WHERE id = ?
        """, (new_end_time, auction_id))
        flash(f'Auction time extended by {EXTENSION_TIME.seconds // 60} minutes!', 'info')

     flash('Bid placed successfully!', 'success')
    return redirect(url_for('auction_details', auction_id=auction_id))
    # Place the bid
    cursor.execute("INSERT INTO bids (auction_id, bidder_id, amount) VALUES (?, ?, ?)",
                   (auction_id, session['user_id'], bid_amount))
    cursor.execute("UPDATE auctions SET current_price = ?, highest_bidder_id = ? WHERE id = ?",
                   (bid_amount, session['user_id'], auction_id))
    conn.commit()
    conn.close()
    flash('Bid placed successfully!', 'success')
    return redirect(url_for('auction_details', auction_id=auction_id))
    
    # Validate bid amount
    if bid_amount <= current_price:
        flash('Your bid must be higher than the current price.', 'danger')
        return redirect(url_for('auction_details', auction_id=auction_id))

    # Prevent users from bidding on their own equipment
    cursor.execute("""
        SELECT owner_id FROM equipment WHERE id = ?
    """, (equipment_id,))
    owner_id = cursor.fetchone()[0]
    if owner_id == session['user_id']:
        flash('You cannot bid on your own equipment.', 'danger')
        return redirect(url_for('auction_details', auction_id=auction_id))
