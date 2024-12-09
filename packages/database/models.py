from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, backref

from .database import Base

# Many-to-Many association table
user_servers = Table(
    "user_servers",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("server_id", Integer, ForeignKey("servers.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    display_name = Column(String)
    discord_id = Column(Integer, nullable=False, index=True, unique=True)
    join_date = Column(DateTime, default=datetime.utcnow)
    admin = Column(Boolean, default=False)
    balance = Column(Integer, nullable=False, default=10000)

    contracts_as_user = relationship(
        'Contracts',
        back_populates='user',
        foreign_keys='Contracts.user_id'
    )
    contracts_as_contractor = relationship(
        'Contracts',
        back_populates='contractor',
        foreign_keys='Contracts.contractor_id'
    )
    properties = relationship(
        'Properties',
        back_populates='owner',
        foreign_keys='Properties.user_id'
    )
    auctions_as_highest_bidder = relationship(
        'Auction',
        back_populates='highest_bidder_user',
        foreign_keys='Auction.highest_bidder'
    )


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=True)
    name = Column(String, nullable=False)
    map = Column(String, nullable=False)

    properties = relationship(
        'Properties',
        back_populates='server'
    )
    auctions = relationship(
        'Auction',
        back_populates='server'
    )
    contracts = relationship(
        'Contracts',
        back_populates='server'
    )


class Properties(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"), nullable=False)
    property_number = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    image = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    server = relationship(
        'Server',
        back_populates='properties'
    )
    owner = relationship(
        'User',
        back_populates='properties'
    )


class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    cost = Column(Integer)
    timeout = Column(DateTime, nullable=False)
    highest_bidder = Column(Integer, ForeignKey("users.id"), nullable=True)

    server = relationship(
        'Server',
        back_populates='auctions'
    )
    property = relationship(
        'Properties',
        backref=backref('auctions', cascade='all, delete-orphan')
    )
    highest_bidder_user = relationship(
        'User',
        back_populates='auctions_as_highest_bidder'
    )


class Contracts(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("servers.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    contractor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='contracts_as_user'
    )
    contractor = relationship(
        'User',
        foreign_keys=[contractor_id],
        back_populates='contracts_as_contractor'
    )
    server = relationship(
        'Server',
        back_populates='contracts'
    )
