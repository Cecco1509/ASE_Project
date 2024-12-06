from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app import db

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
