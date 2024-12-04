from datetime import datetime

def end_auctions():
    current_time = datetime.utcnow()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Update auctions that have passed the end time
    cursor.execute("""
        UPDATE auctions
        SET status = 'closed'
        WHERE end_time <= ? AND status = 'active'
    """, (current_time,))

    conn.commit()
    conn.close()
def close_auctions():
    current_time = datetime.utcnow()

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch auctions that need to be closed
    cursor.execute("""
        SELECT a.id, a.highest_bidder_id, e.name
        FROM auctions a
        JOIN equipment e ON a.equipment_id = e.id
        WHERE a.end_time <= ? AND a.status = 'active'
    """, (current_time,))
    expired_auctions = cursor.fetchall()

    # Close auctions
    cursor.execute("""
        UPDATE auctions SET status = 'closed'
        WHERE end_time <= ? AND status = 'active'
    """, (current_time,))

    conn.commit()
    conn.close()

    # Notify winners
    for auction in expired_auctions:
        auction_id, highest_bidder_id, equipment_name = auction
        if highest_bidder_id:
            send_notification(highest_bidder_id, f"You won the auction for {equipment_name}!")

def send_notification(user_id, message):
    # Example function to send notifications (extend as needed)
    print(f"Notification to User {user_id}: {message}")
