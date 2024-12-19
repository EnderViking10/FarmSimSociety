from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Association Table for Many-to-Many Relationship
user_servers = db.Table(
    "user_servers",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("server_id", db.Integer, db.ForeignKey("servers.id", ondelete="CASCADE"), primary_key=True),
)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(50))
    display_name = db.Column(db.String(100))
    discord_id = db.Column(db.BigInteger, nullable=False, index=True, unique=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    credit_score = db.Column(db.Integer, default=650)
    net_worth = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    contracts_as_user = db.relationship("Contracts", back_populates="user", foreign_keys="Contracts.user_id")
    contracts_as_contractor = db.relationship("Contracts", back_populates="contractor", foreign_keys="Contracts.contractor_id")
    properties = db.relationship("Properties", back_populates="owner", foreign_keys="Properties.user_id")
    auctions_as_highest_bidder = db.relationship("Auction", back_populates="highest_bidder_user", foreign_keys="Auction.highest_bidder")
    transactions = db.relationship("Transaction", back_populates="transaction_user", foreign_keys="Transaction.user_id")
    sent_transactions = db.relationship("Transaction", foreign_keys="Transaction.sender_id")
    received_transactions = db.relationship("Transaction", foreign_keys="Transaction.recipient_id")
    savings = db.relationship("Savings", back_populates="user")
    loans = db.relationship("Loan", back_populates="user")
    servers = db.relationship("Server", secondary=user_servers, back_populates="users")
    assets = db.relationship("Asset", back_populates="owner")

    def __repr__(self):
        return (f"<User(id={self.id}, username='{self.username}', display_name='{self.display_name}', "
                f"discord_id={self.discord_id}, balance={self.balance}, credit_score={self.credit_score})>")

# Auction model
class Auction(db.Model):
    __tablename__ = "auctions"

    id = db.Column(db.Integer, primary_key=True, index=True)
    server_id = db.Column(db.Integer, db.ForeignKey("servers.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False)
    cost = db.Column(db.Integer)
    timeout = db.Column(db.DateTime, nullable=False)
    highest_bidder = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Relationships
    server = db.relationship("Server", back_populates="auctions")
    property = db.relationship("Properties", backref=db.backref("auctions", cascade="all, delete-orphan"))
    highest_bidder_user = db.relationship("User", back_populates="auctions_as_highest_bidder")

    def __repr__(self):
        return (f"<Auction(id={self.id}, server_id={self.server_id}, property_id={self.property_id}, "
                f"cost={self.cost}, timeout={self.timeout}, highest_bidder={self.highest_bidder})>")

# Transaction model
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # "deposit", "withdraw", "transfer-in", "transfer-out"
    action = db.Column(db.String(50), nullable=True)  # "outgoing", "incoming"
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    transaction_user = db.relationship("User", back_populates="transactions", foreign_keys=[user_id])
    sender_user = db.relationship("User", foreign_keys=[sender_id])
    recipient_user = db.relationship("User", foreign_keys=[recipient_id])

    def __repr__(self):
        return (f"<Transaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, type='{self.type}', "
                f"recipient_id={self.recipient_id}, sender_id={self.sender_id}, timestamp={self.timestamp})>")

# Loan model
class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)  # Annual interest rate (e.g., 4.5%)
    term = db.Column(db.Integer, nullable=False)  # Term in months
    monthly_payment = db.Column(db.Float, nullable=False)
    remaining_balance = db.Column(db.Float, nullable=False)
    next_payment_due = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='active')  # 'active', 'paid', etc.

    # Back reference to User model
    user = db.relationship("User", back_populates="loans")

    def __repr__(self):
        return (f"<Loan(id={self.id}, user_id={self.user_id}, amount={self.amount}, "
                f"interest_rate={self.interest_rate}, term={self.term}, status={self.status})>")

# Asset model
class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True, index=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(50), nullable=False)
    server_id = db.Column(db.Integer, db.ForeignKey("servers.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    owner = db.relationship("User", back_populates="assets")

    def __repr__(self):
        return f"<Asset(id={self.id}, type={self.type}, name={self.name}, description={self.description})>"

# Server model (added for context)
class Server(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True, index=True)
    ip = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    map = db.Column(db.String(50), nullable=False)

    # Relationships
    properties = db.relationship("Properties", back_populates="server")
    auctions = db.relationship("Auction", back_populates="server")
    contracts = db.relationship("Contracts", back_populates="server")
    users = db.relationship("User", secondary=user_servers, back_populates="servers")

    def __repr__(self):
        return f"<Server(id={self.id}, name='{self.name}', ip='{self.ip}', map='{self.map}')>"

