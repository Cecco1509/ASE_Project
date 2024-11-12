
import pyodbc
def setup():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        f'SERVER=authdatabase,1433;'
                        f'DATABASE=master;'
                        f'UID=sa;'
                        f'PWD=Password1.')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'AuthDatabase') \
    BEGIN CREATE DATABASE AuthDatabase; END")
    cursor.close()
    conn.close()

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        f'SERVER=gachadatabase,1433;'
                        f'DATABASE=master;'
                        f'UID=sa;'
                        f'PWD=Password1.')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'GachaDatabase') \
    BEGIN CREATE DATABASE GachaDatabase; END")
    cursor.close()
    conn.close()

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        f'SERVER=userdatabase,1433;'
                        f'DATABASE=master;'
                        f'UID=sa;'
                        f'PWD=Password1.')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'UserDatabase') \
    BEGIN CREATE DATABASE UserDatabase; END")
    cursor.close()
    conn.close()

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        f'SERVER=paymentdatabase,1433;'
                        f'DATABASE=master;'
                        f'UID=sa;'
                        f'PWD=Password1.')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'PaymentDatabase') \
    BEGIN CREATE DATABASE PaymentDatabase; END")
    cursor.close()
    conn.close()

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        f'SERVER=auctiondatabase,1433;'
                        f'DATABASE=master;'
                        f'UID=sa;'
                        f'PWD=Password1.')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'AuctionDatabase') \
    BEGIN CREATE DATABASE AuctionDatabase; END")
    cursor.close()
    conn.close()

    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                        f'SERVER=transactiondatabase,1433;'
                        f'DATABASE=master;'
                        f'UID=sa;'
                        f'PWD=Password1.')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TransactionDatabase') \
    BEGIN CREATE DATABASE TransactionDatabase; END")
    cursor.close()
    conn.close()