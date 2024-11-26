from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from app import db

class Account(db.Model):
    __tablename__ = 'account'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] 
    password: Mapped[str]
    salt: Mapped[str]
    role: Mapped[str]
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
    salt: Mapped[str]
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }