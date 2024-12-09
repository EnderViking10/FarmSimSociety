from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

user_servers = db.Table(
    "user_servers",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("server_id", db.Integer, db.ForeignKey("servers.id", ondelete="CASCADE"), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String)
    display_name = db.Column(db.String)
    discord_id = db.Column(db.Integer, nullable=False, index=True, unique=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Integer, nullable=False, default=10000)
    credit_score = db.Column(db.Integer, default=650)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    contracts_as_user = db.relationship("Contracts", back_populates="user", foreign_keys="Contracts.user_id")
    contracts_as_contractor = db.relationship("Contracts", back_populates="contractor",
                                              foreign_keys="Contracts.contractor_id")
    properties = db.relationship("Properties", back_populates="owner", foreign_keys="Properties.user_id")
    auctions_as_highest_bidder = db.relationship("Auction", back_populates="highest_bidder_user",
                                                 foreign_keys="Auction.highest_bidder")

    # Updated relationships for transactions
    transactions = db.relationship('Transaction', backref='user', lazy=True, foreign_keys="Transaction.user_id")
    sent_transactions = db.relationship('Transaction', lazy=True, foreign_keys="Transaction.sender_id")
    received_transactions = db.relationship('Transaction', lazy=True, foreign_keys="Transaction.recipient_id")

    def __repr__(self):
        return (f"<User(id={self.id}, username='{self.username}', display_name='{self.display_name}', "
                f"discord_id={self.discord_id}, balance={self.balance}, credit_score={self.credit_score})>")


class Server(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True, index=True)
    ip = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    map = db.Column(db.String, nullable=False)

    properties = db.relationship("Properties", back_populates="server")
    auctions = db.relationship("Auction", back_populates="server")
    contracts = db.relationship("Contracts", back_populates="server")

    def __repr__(self):
        return f"<Server(id={self.id}, name='{self.name}', ip='{self.ip}', map='{self.map}')>"


class Properties(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True, index=True)
    server_id = db.Column(db.Integer, db.ForeignKey("servers.id"), nullable=False)
    property_number = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    image = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    server = db.relationship("Server", back_populates="properties")
    owner = db.relationship("User", back_populates="properties")

    def __repr__(self):
        return (f"<Properties(id={self.id}, server_id={self.server_id}, property_number={self.property_number}, "
                f"user_id={self.user_id}, size={self.size}, price={self.price})>")


class Auction(db.Model):
    __tablename__ = "auctions"

    id = db.Column(db.Integer, primary_key=True, index=True)
    server_id = db.Column(db.Integer, db.ForeignKey("servers.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    cost = db.Column(db.Integer)
    timeout = db.Column(db.DateTime, nullable=False)
    highest_bidder = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    server = db.relationship("Server", back_populates="auctions")
    property = db.relationship("Properties", backref=db.backref("auctions", cascade="all, delete-orphan"))
    highest_bidder_user = db.relationship("User", back_populates="auctions_as_highest_bidder")

    def __repr__(self):
        return (f"<Auction(id={self.id}, server_id={self.server_id}, property_id={self.property_id}, "
                f"cost={self.cost}, timeout={self.timeout}, highest_bidder={self.highest_bidder})>")


class Contracts(db.Model):
    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey("servers.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    payout = db.Column(db.Integer, nullable=True)
    type = db.Column(db.String, nullable=True)

    user = db.relationship("User", foreign_keys=[user_id], back_populates="contracts_as_user")
    contractor = db.relationship("User", foreign_keys=[contractor_id], back_populates="contracts_as_contractor")
    server = db.relationship("Server", back_populates="contracts")

    def __repr__(self):
        return (f"<Contracts(id={self.id}, user_id={self.user_id}, server_id={self.server_id}, "
                f"title='{self.title}', description='{self.description}', status='{self.status}', "
                f"price={self.price}, contractor_id={self.contractor_id}, start_time={self.start_time}, "
                f"end_time={self.end_time}, payout={self.payout}, type='{self.type}')>")


class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    principal = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)  # Annual interest rate
    term_years = db.Column(db.Integer, nullable=False)  # Loan term in years
    balance = db.Column(db.Float, nullable=False)  # Remaining balance
    status = db.Column(db.String(20), default="active")  # "active", "paid"
    due_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f"<Loan(id={self.id}, user_id={self.user_id}, principal={self.principal}, "
                f"interest_rate={self.interest_rate}, term_years={self.term_years}, balance={self.balance}, "
                f"status='{self.status}', due_date={self.due_date})>")


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # Primary transaction owner
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # "deposit", "withdraw", "transfer-in", "transfer-out"
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # For transfers
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # For transfers
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, type='{self.type}', "
                f"recipient_id={self.recipient_id}, sender_id={self.sender_id}, timestamp={self.timestamp})>")
