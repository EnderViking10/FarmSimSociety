from sqlalchemy.orm import Session

from .models import User, Auction, Server, Properties


class UserRepository:
    @staticmethod
    def create_user(session: Session, username: str, discord_id: int, admin: bool = False) -> User:
        user = User(username=username, discord_id=discord_id, admin=admin)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def get_user_by_discord_id(session: Session, discord_id: int) -> User | None:
        return session.query(User).filter(User.discord_id == discord_id).first()

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> User | None:
        return session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def add_money(session: Session, discord_id: int, amount: int) -> None:
        user = UserRepository.get_user_by_discord_id(session, discord_id)
        user.balance += amount
        session.commit()

    @staticmethod
    def remove_money(session: Session, discord_id: int, amount: int) -> None:
        user = UserRepository.get_user_by_discord_id(session, discord_id)
        user.balance -= amount
        session.commit()

    @staticmethod
    def update_username(session: Session, discord_id: int, username: str) -> None:
        user = UserRepository.get_user_by_discord_id(session, discord_id)
        user.username = username
        session.commit()


class AuctionRepository:
    @staticmethod
    def create_auction(session: Session, server_id: int, property_id: int) -> Auction | None:
        auction = Auction(server_id=server_id, property_id=property_id)
        session.add(auction)
        session.commit()
        session.refresh(auction)
        return auction

    @staticmethod
    def get_auction_by_id(session: Session, auction_id: int) -> Auction | None:
        return session.query(Auction).filter(Auction.id == auction_id).first()


class ServerRepository:
    @staticmethod
    def create_server(session: Session, ip: str, name: str, map: str) -> Server:
        server = Server(ip=ip, name=name, map=map)
        session.add(server)
        session.commit()
        session.refresh(server)
        return server

    @staticmethod
    def get_server_by_id(session: Session, server_id: int) -> Server | None:
        return session.query(Server).filter(Server.id == server_id).first()


class PropertyRepository:
    @staticmethod
    def create_property(session: Session, server_id: int, user_id: int, image: str, size: int,
                        price: int) -> Properties | None:
        properties = Properties(server_id=server_id, user_id=user_id, image=image, size=size, price=price)
        session.add(properties)
        session.commit()
        session.refresh(properties)
        return properties
