from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from enums import UserStatus, GachaSource, AuctionStatus
from app import db

class Account(db.Model):
    __tablename__ = 'account'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str] 

class Admin(db.Model):
    __tablename__ = 'admin'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str]

class User(db.Model):
    __bind_key__ = 'userDatabase'
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    authId: Mapped[int]
    ingameCurrency: Mapped[float]
    profilePicture: Mapped[str]
    registrationDate: Mapped[datetime]
    status: Mapped[UserStatus]

class Gacha(db.Model):
    __bind_key__ = 'gachaDatabase'
    __tablename__ = 'gacha'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    image: Mapped[str]
    rarityPercent: Mapped[float]
    description: Mapped[str]

class GachaCollection(db.Model):
    __bind_key__ = 'gachaDatabase'
    __tablename__ = 'gachaCollection'
    id: Mapped[int] = mapped_column(primary_key=True)
    gachaId: Mapped[int] = mapped_column(ForeignKey("gacha.id"))
    userId: Mapped[int]
    timestamp: Mapped[datetime]
    source: Mapped[GachaSource]

class Auction(db.Model):
    __bind_key__ = 'auctionDatabase'
    __tablename__ = 'auction'
    id: Mapped[int] = mapped_column(primary_key=True)
    gachaCollectionId: Mapped[int]
    auctionStart: Mapped[datetime]
    auctionEnd: Mapped[datetime]
    minimumBid: Mapped[float]
    timestamp: Mapped[datetime]
    status: Mapped[AuctionStatus]

class AuctionBid(db.Model):
    __bind_key__ = 'auctionDatabase'
    __tablename__ = 'auctionBid'
    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int]
    bidAmount: Mapped[float]
    auctionId: Mapped[int] = mapped_column(ForeignKey("auction.id"))
    timestamp: Mapped[datetime]

class CurrencyTransaction(db.Model):
    __bind_key__ = 'paymentDatabase'
    __tablename__ = 'currencyTransaction'
    id: Mapped[int] = mapped_column(primary_key=True)
    userId: Mapped[int]
    realMount: Mapped[float]
    ingameMount: Mapped[float]
    timestamp: Mapped[datetime]

class AuctionTransaction(db.Model):
    __bind_key__ = 'transactionDatabase'
    __tablename__ = 'auctionTransaction'
    id: Mapped[int] = mapped_column(primary_key=True)
    sellerId: Mapped[int]
    buyerId: Mapped[int]
    auctionBidId: Mapped[int]
    timestamp: Mapped[datetime]