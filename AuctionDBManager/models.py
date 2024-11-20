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
