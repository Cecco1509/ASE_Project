from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app import db
from enum import Enum

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
