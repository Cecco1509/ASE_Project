from flask import Flask, request, make_response 
from enums import UserStatus, GachaSource, AuctionStatus

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
import pyodbc

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Password1.@sqldatabase:1433/AuthDatabase?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_BINDS'] = {
    'gachaDatabase': 'mssql+pyodbc://sa:Password1.@sqldatabase:1433/GachaDatabase?driver=ODBC+Driver+17+for+SQL+Server',
    'userDatabase': 'mssql+pyodbc://sa:Password1.@sqldatabase:1433/UserDatabase?driver=ODBC+Driver+17+for+SQL+Server',
    'paymentDatabase': 'mssql+pyodbc://sa:Password1.@sqldatabase:1433/PaymentDatabase?driver=ODBC+Driver+17+for+SQL+Server',
    'auctionDatabase': 'mssql+pyodbc://sa:Password1.@sqldatabase:1433/AuctionDatabase?driver=ODBC+Driver+17+for+SQL+Server',
    'transactionDatabase': 'mssql+pyodbc://sa:Password1.@sqldatabase:1433/TransactionDatabase?driver=ODBC+Driver+17+for+SQL+Server'
}

#SQLAlchemy.init_app(app)

class Base(DeclarativeBase):
    pass

conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                      f'SERVER=sqldatabase,1433;'
                      f'DATABASE=master;'
                      f'UID=sa;'
                      f'PWD=Password1.')
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'AuthDatabase') \
BEGIN CREATE DATABASE AuthDatabase; END")
cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'GachaDatabase') \
BEGIN CREATE DATABASE GachaDatabase; END")
cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'UserDatabase') \
BEGIN CREATE DATABASE UserDatabase; END")
cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'PaymentDatabase') \
BEGIN CREATE DATABASE PaymentDatabase; END")
cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'AuctionDatabase') \
BEGIN CREATE DATABASE AuctionDatabase; END")
cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TransactionDatabase') \
BEGIN CREATE DATABASE TransactionDatabase; END")
cursor.close()
conn.close()

db = SQLAlchemy(app)


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)