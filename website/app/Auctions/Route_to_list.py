from datetime import datetime, timedelta

@main.route('/create_auction', methods=['GET', 'POST'])
@login_required
def create_auction():
    if request.method == 'POST':
        equipment_id = request.form['equipment_id']
        starting_price = float(request.form['starting_price'])
        current_time = datetime.utcnow()
        end_time = current_time + timedelta(hours=24)  # Set auction to end in 24 hours
        # Validate starting price
        if starting_price <= 0:
            flash('Starting price must be greater than 0.', 'danger')
            return redirect(url_for('create_auction'))

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO auctions (equipment_id, starting_price, current_price, end_time, status)
            VALUES (?, ?, ?, ?, 'active')
        """, (equipment_id, starting_price, starting_price, end_time))

        conn.commit()
        conn.close()
        flash('Auction created successfully with a 24-hour limit!', 'success')
        return redirect(url_for('list_auctions'))
    
    # Fetch equipment owned by the logged-in user
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name FROM equipment WHERE owner_id = ?
    """, (session['user_id'],))
    equipment = cursor.fetchall()
    conn.close()
     
      # Check if the equipment belongs to the user
        cursor.execute("""
            SELECT id FROM equipment WHERE id = ? AND owner_id = ?
        """, (equipment_id, session['user_id']))
        equipment = cursor.fetchone()
        if not equipment:
            flash('You can only list your own equipment.', 'danger')
            return redirect(url_for('create_auction'))

        # Check if equipment is already in an active auction
        cursor.execute("""
            SELECT id FROM auctions WHERE equipment_id = ? AND status = 'active'
        """, (equipment_id,))
        active_auction = cursor.fetchone()
        if active_auction:
            flash('This equipment is already listed in an active auction.', 'danger')
            return redirect(url_for('create_auction'))

        # Set the auction to end in 24 hours
        end_time = datetime.utcnow() + timedelta(hours=24)
        cursor.execute("""
            INSERT INTO auctions (equipment_id, starting_price, current_price, end_time, status)
            VALUES (?, ?, ?, ?, 'active')
        """, (equipment_id, starting_price, starting_price, end_time))
        conn.commit()
        conn.close()

        flash('Auction created successfully!', 'success')
        return redirect(url_for('list_auctions'))

    # Fetch user's equipment
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name FROM equipment WHERE owner_id = ?
    """, (session['user_id'],))
    equipment = cursor.fetchall()
    conn.close()

    return render_template('create_auction.html', equipment=equipment)