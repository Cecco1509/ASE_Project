from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app import db
from enum import Enum

class AuctionStatus(Enum):
    ACTIVE = 1
    PASSED = 2
    UNKNOWN = 3

class Auction(db.Model):
    __tablename__ = 'auction'
    id: Mapped[int] = mapped_column(primary_key=True)
    gachaCollectionId: Mapped[int]
    createdBy: Mapped[int]
    auctionStart: Mapped[datetime]
    auctionEnd: Mapped[datetime]
    minimumBid: Mapped[float]
    timestamp: Mapped[datetime]
    status: Mapped[AuctionStatus]
    def to_dict(self):
        return {
            'id': self.id,
            'gachaCollectionId': self.gachaCollectionId,
            'auctionStart': self.auctionStart,
            'auctionEnd': self.auctionEnd,
            'minimumBid': self.minimumBid,
            'timestamp': self.timestamp,
            'status': self.status.name
        }
    
    def from_dict(data):
        return Auction(
            gachaCollectionId=data['gachaCollectionId'],
            auctionStart=data['auctionStart'],
            auctionEnd=data['auctionEnd'],
            minimumBid=data['minimumBid'],
            timestamp=data['timestamp'],
            status=AuctionStatus(data['status'])
        )


class Account(db.Model):
    __tablename__ = 'account'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str]
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }

class Admin(db.Model):
    __tablename__ = 'admin'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str]
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
class AuctionBid(db.Model):
    __tablename__ = 'auctionBid'
    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int]
    bidAmount: Mapped[float]
    auctionId: Mapped[int] = mapped_column(ForeignKey("auction.id"))
    timestamp: Mapped[datetime]
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'bidAmount': self.bidAmount,
            'auctionId': self.auctionId,
            'timestamp': self.timestamp
        }
    
    def from_dict(data):
        return AuctionBid(
            userId=data['userId'],
            bidAmount=data['bidAmount'],
            auctionId=data['auctionId'],
            timestamp=data['timestamp']
        )
    

class GachaSource(Enum):
    ROLL = 1
    AUCTION = 2
    UNKNOWN = 3

class Gacha(db.Model):
    __tablename__ = 'gacha'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    image: Mapped[str]
    rarityPercent: Mapped[float]
    description: Mapped[str]
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'rarityPercent': self.rarityPercent
        }
        

class GachaCollection(db.Model):
    __tablename__ = 'gachaCollection'
    id: Mapped[int] = mapped_column(primary_key=True)
    gachaId: Mapped[int] = mapped_column(ForeignKey("gacha.id"))
    userId: Mapped[int]
    timestamp: Mapped[datetime]
    source: Mapped[GachaSource]
    def to_dict(self):
        return {
            'id': self.id,
            'gachaId': self.gachaId,
            'userId': self.userId,
            'timestamp': self.timestamp,
            'source': self.source.name
        }
    
    def from_dict(data):
        return GachaCollection(
            gachaId=data['gachaId'],
            userId=data['userId'],
            timestamp=data['timestamp'],
            source=GachaSource(data['source'])
        )


class CurrencyTransaction(db.Model):
    __tablename__ = 'currencyTransaction'
    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int]
    realAmount: Mapped[float]
    ingameAmount: Mapped[float]
    timestamp: Mapped[datetime]
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'realAmount': self.realAmount,
            'ingameAmount': self.ingameAmount,
            'timestamp': self.timestamp
        }
    

class AuctionTransaction(db.Model):
    __tablename__ = 'auctionTransaction'
    id: Mapped[int] = mapped_column(primary_key=True)
    sellerId: Mapped[int]
    buyerId: Mapped[int]
    auctionBidId: Mapped[int]
    timestamp: Mapped[datetime]
    def to_dict(self):
        return {
            'id': self.id,
            'sellerId': self.sellerId,
            'buyerId': self.buyerId,
            'auctionBidId': self.auctionBidId,
            'timestamp': self.timestamp
        }
    

class UserStatus(Enum):
    ACTIVE = 1
    BANNED = 2
    UNKNOWN = 3

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    authId: Mapped[int]
    ingameCurrency: Mapped[float]
    profilePicture: Mapped[str]
    registrationDate: Mapped[datetime]
    status: Mapped[UserStatus]
    def to_dict(self):
        return {
            'id': self.id,
            'authId': self.authId,
            'ingameCurrency': self.ingameCurrency,
            'profilePicture': self.profilePicture,
            'registrationDate': self.registrationDate,
            'status': self.status.name
        }
