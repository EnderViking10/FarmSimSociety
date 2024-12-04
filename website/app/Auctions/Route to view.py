@main.route('/auction/<int:auction_id>')
def auction_details(auction_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Fetch auction details
    cursor.execute("""
        SELECT a.id, e.name, e.description, e.image_url, a.starting_price, a.current_price, a.end_time, u.username
        FROM auctions a
        JOIN equipment e ON a.equipment_id = e.id
        LEFT JOIN users u ON a.highest_bidder_id = u.id
        WHERE a.id = ?
    """, (auction_id,))
    auction = cursor.fetchone()
    
    # Fetch bids for the auction
    cursor.execute("""
        SELECT b.amount, b.bid_time, u.username
        FROM bids b
        JOIN users u ON b.bidder_id = u.id
        WHERE b.auction_id = ?
        ORDER BY b.bid_time DESC
    """, (auction_id,))
    bids = cursor.fetchall()
    
    conn.close()
    return render_template('auction_details.html', auction=auction, bids=bids)
