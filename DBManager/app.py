from flask import Flask, request, make_response

from flask_sqlalchemy import SQLAlchemy
import pyodbc
from dbsetup import setup

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:Password1.@authdatabase:1433/AuthDatabase?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_BINDS'] = {
    'gachaDatabase': 'mssql+pyodbc://sa:Password1.@gachadatabase:1433/GachaDatabase?driver=ODBC+Driver+17+for+SQL+Server',
    'userDatabase': 'mssql+pyodbc://sa:Password1.@userdatabase:1433/UserDatabase?driver=ODBC+Driver+17+for+SQL+Server',
    'paymentDatabase': 'mssql+pyodbc://sa:Password1.@paymentdatabase:1433/PaymentDatabase?driver=ODBC+Driver+17+for+SQL+Server',
    'auctionDatabase': 'mssql+pyodbc://sa:Password1.@auctiondatabase:1433/AuctionDatabase?driver=ODBC+Driver+17+for+SQL+Server',
    'transactionDatabase': 'mssql+pyodbc://sa:Password1.@transactiondatabase:1433/TransactionDatabase?driver=ODBC+Driver+17+for+SQL+Server'
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