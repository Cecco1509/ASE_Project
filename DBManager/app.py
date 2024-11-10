from flask import Flask, request, make_response 

from flask_sqlalchemy import SQLAlchemy
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
import entities

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)