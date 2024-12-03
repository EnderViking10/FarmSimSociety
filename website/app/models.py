from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from app import db

# Many-to-Many association table
user_servers = db.Table(
    "user_servers",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    db.Column("server_id", db.Integer, db.ForeignKey("servers.id", ondelete="CASCADE"), primary_key=True),
)


# Example model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String)
    discord_id = db.Column(db.Integer, nullable=False, index=True, unique=True)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    @classmethod
    def get_user(cls, discord_id: int):
        return cls.query.filter_by(discord_id=discord_id).first()

    @classmethod
    def update_username(cls, discord_id: int, username: str):
        user = cls.query.filter_by(discord_id=discord_id).first()
        if user:
            user.username = username
            db.session.commit()
        return user

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, discord_id={self.discord_id})>"


class Bank(db.Model):
    __tablename__ = "bank"

    id = db.Column(db.Integer, primary_key=True, index=True)
    discord_id = db.Column(db.Integer, db.ForeignKey("users.discord_id"), nullable=False, unique=True)
    balance = db.Column(db.Integer, nullable=False, default=10000)

    @classmethod
    def get_bank(cls, discord_id: int):
        return cls.query.filter_by(discord_id=discord_id).first()

    def __repr__(self):
        return f"<Bank(id={self.id}, discord_id={self.discord_id}, balance={self.balance})>"


class Servers(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True, index=True)
    ip = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    map = db.Column(db.String, nullable=False)

    @classmethod
    def get_server(cls, server_id: int):
        return cls.query.filter_by(id=server_id).first()

    @classmethod
    def add_server(cls, server_id: int, server_ip: str, server_name: str, server_map: str):
        new_server = Servers(id=server_id, ip=server_ip, name=server_name, map=server_map)
        db.session.add(new_server)
        db.session.commit()
        return new_server

    @classmethod
    def update_server_ip(cls, server_id: int, ip: str):
        server = cls.query.filter_by(id=server_id).first()
        if server:
            server.ip = ip
            db.session.commit()
        return server

    @classmethod
    def update_server_name(cls, server_id: int, name: str):
        server = cls.query.filter_by(id=server_id).first()
        if server:
            server.name = name
            db.session.commit()
        return server

    @classmethod
    def update_server_map(cls, server_id: int, map: str):
        server = cls.query.filter_by(id=server_id).first()
        if server:
            server.map = map
            db.session.commit()
        return server

    def __repr__(self):
        return f"<Server(id={self.id}, ip={self.ip})>"
