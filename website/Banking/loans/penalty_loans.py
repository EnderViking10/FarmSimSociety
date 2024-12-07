def apply_penalty(loan):
    # Add penalty to the balance (e.g., 5% late fee)
    penalty_fee = loan.balance * 0.05
    loan.penalty += penalty_fee
    loan.balance += penalty_fee  # Add penalty to the loan balance
def calculate_penalty(loan):
    overdue_days = (datetime.utcnow() - loan.due_date).days
    if overdue_days > 0:
        penalty_percentage = 0.05  # 5% fee for every overdue month
        penalty_fee = loan.balance * penalty_percentage * (overdue_days // 30)
        loan.penalty += penalty_fee
        loan.balance += penalty_fee
    db.session.commit()