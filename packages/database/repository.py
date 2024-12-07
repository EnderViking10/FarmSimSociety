from typing import List, Type

from datetime import datetime
from sqlalchemy.orm import Session

from .models import User, Auction, Server, Properties, Contracts


class UserRepository:
    @staticmethod
    def create_user(session: Session, username: str, display_name: str, discord_id: int, admin: bool = False) -> User:
        user = User(username=username, display_name=display_name, discord_id=discord_id, admin=admin)
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

    @staticmethod
    def update_display_name(session: Session, discord_id: int, display_name: str) -> None:
        user = UserRepository.get_user_by_discord_id(session, discord_id)
        user.display_name = display_name
        session.commit()
        session.refresh(user)


class AuctionRepository:
    @staticmethod
    def create_auction(session: Session, server_id: int, property_id: int, cost: int,
                       timeout: datetime) -> Auction | None:
        auction = Auction(server_id=server_id, property_id=property_id, cost=cost, timeout=timeout)
        session.add(auction)
        session.commit()
        session.refresh(auction)
        return auction

    @staticmethod
    def get_auction_by_id(session: Session, auction_id: int) -> Auction | None:
        return session.query(Auction).filter(Auction.id == auction_id).first()

    @staticmethod
    def get_all_auctions(session: Session) -> list[Type[Auction]]:
        return session.query(Auction).all()

    @staticmethod
    def set_timeout(session: Session, auction_id: int, auction_time: int) -> None:
        auction = AuctionRepository.get_auction_by_id(session, auction_id)
        auction.auction_time = auction_time
        session.commit()
        session.refresh(auction)

    @staticmethod
    def set_highest_bidder(session: Session, auction_id: int, user_id: int, auction_bid: int) -> None:
        auction = AuctionRepository.get_auction_by_id(session, auction_id)
        auction.auction_bid = auction_bid
        auction.highest_bidder = user_id
        session.commit()
        session.refresh(auction)


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
    def create_property(session: Session, server_id: int, property_number: int, image: str,
                        size: int, price: int, user_id: int = None) -> Properties | None:
        properties = Properties(server_id=server_id, user_id=user_id, property_number=property_number, image=image,
                                size=size, price=price)
        session.add(properties)
        session.commit()
        session.refresh(properties)
        return properties

    @staticmethod
    def get_property(session: Session, server_id: int, property_id: int) -> Properties | None:
        return session.query(Properties).filter(Properties.server_id == server_id, Properties.id == property_id).first()


class ContractRepository:
    @staticmethod
    def create_contract(session: Session, user_id: int, server_id: int, title: str, description: str,
                        price: int) -> Contracts:
        contract = Contracts(user_id=user_id, server_id=server_id, title=title, description=description,
                             status='pending', price=price)

        session.add(contract)
        session.commit()
        session.refresh(contract)
        return contract

    @staticmethod
    def get_all_contracts(session: Session) -> list[Type[Contracts]]:
        return session.query(Contracts).all()

    @staticmethod
    def set_price(session: Session, contract_id: int, price: int) -> None:
        contract = ContractRepository.get_property(session, contract_id)
        contract.price = price
        session.commit()
        session.refresh(contract)

    @staticmethod
    def set_status(session: Session, contract_id: int, status: str) -> None:
        contract = ContractRepository.get_property(session, contract_id)
        contract.status = status
        session.commit()
        session.refresh(contract)

    @staticmethod
    def set_description(session: Session, contract_id: int, description: str) -> None:
        contract = ContractRepository.get_property(session, contract_id)
        contract.description = description
        session.commit()
        session.refresh(contract)

    @staticmethod
    def set_title(session: Session, contract_id: int, title: str) -> None:
        contract = ContractRepository.get_property(session, contract_id)
        contract.title = title
        session.commit()
        session.refresh(contract)

    @staticmethod
    def set_contractor_id(session: Session, contract_id: int, contractor_id: int) -> None:
        contract = ContractRepository.get_property(session, contract_id)
        contract.contractor_id = contractor_id
        session.commit()
        session.refresh(contract)
