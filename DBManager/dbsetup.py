
import pyodbc
from python_json_config import ConfigBuilder

builder = ConfigBuilder()
config = builder.parse_config('./config.json')

def single_db_setup(db):
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                            f'SERVER={db.server},{db.port};'
                            f'DATABASE=master;'
                            f'UID={db.username};'
                            f'PWD={db.password}')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{db.name}') \
        BEGIN CREATE DATABASE {db.name}; END")
        cursor.close()
        conn.close()
    except:
        print(f"Database {db.server}:{db.port} unavailable.")
def setup():
    single_db_setup(config.databases.auth)
    single_db_setup(config.databases.gacha)
    single_db_setup(config.databases.user)
    single_db_setup(config.databases.payment)
    single_db_setup(config.databases.auction)
    single_db_setup(config.databases.transaction)