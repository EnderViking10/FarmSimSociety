from app import app, db
from app.models import SavingsAccount, SavingsTransaction

@app.task
def apply_interest():
    accounts = SavingsAccount.query.all()
    for account in accounts:
        if account.balance > 0:
            interest = account.balance * (account.interest_rate / 12)  # Monthly interest
            account.balance += interest
            db.session.add(SavingsTransaction(account_id=account.id, action='interest', amount=interest))
    db.session.commit()
