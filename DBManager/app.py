from flask import Flask, request, make_response

from flask_sqlalchemy import SQLAlchemy
import pyodbc
from dbsetup import setup
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('./config.json')

def create_connection_string(db):
    return f'mssql+pyodbc://{db.username}:{db.password}@{db.server}:{db.port}/{db.name}?driver=ODBC+Driver+17+for+SQL+Server'

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 


app.config['SQLALCHEMY_DATABASE_URI'] = create_connection_string(config.databases.auth)
app.config['SQLALCHEMY_BINDS'] = {
    'gachaDatabase': create_connection_string(config.databases.gacha),
    'userDatabase': create_connection_string(config.databases.user),
    'paymentDatabase': create_connection_string(config.databases.payment),
    'auctionDatabase': create_connection_string(config.databases.auction),
    'transactionDatabase': create_connection_string(config.databases.transaction)
}

setup()

db = SQLAlchemy(app)
import models
import GachaEndpoints
import AccountEndpoints
import AdminEndpoints
import AuctionEndpoints
import AuctionBidEndpoints
import CurrencyTransactionEndpoints
import UserEndpoints
import GachaCollectionEndpoints

#if __name__ == '__main__':
with app.app_context():
    db.create_all()
app.run(debug=True)