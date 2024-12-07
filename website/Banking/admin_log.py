def log_action(admin_id, action):
    log_entry = AdminActivityLog(admin_id=admin_id, action=action)
    db.session.add(log_entry)
    db.session.commit()
