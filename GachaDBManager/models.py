from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app import db
from enum import Enum

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
