from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app import db

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