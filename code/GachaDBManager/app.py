from flask import Flask, request, make_response

from flask_sqlalchemy import SQLAlchemy
import pyodbc
from python_json_config import ConfigBuilder
import time

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

with open('/run/secrets/db_password', 'r') as file:
    password = file.read().strip()

def create_connection_string(db):
    return f'mssql+pyodbc://{db.username}:{password}@{db.server}:{db.port}/{db.name}?driver=ODBC+Driver+17+for+SQL+Server'

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 


app.config['SQLALCHEMY_DATABASE_URI'] = create_connection_string(config.databases.gacha)
for i in range(config.databases.retries):
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                            f'SERVER={config.databases.gacha.server},{config.databases.gacha.port};'
                            f'DATABASE=master;'
                            f'UID={config.databases.gacha.username};'
                            f'PWD={password};'
                            'Encrypt=yes;TrustServerCertificate=yes')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{config.databases.gacha.name}') \
        BEGIN CREATE DATABASE {config.databases.gacha.name}; END")
        cursor.close()
        conn.close()
    except:
        time.sleep(config.databases.timeout)

db = SQLAlchemy(app)
import models
import GachaEndpoints
import GachaCollectionEndpoints

with app.app_context():
    db.create_all()
    for gacha in models.gacha_items:
        gacha_obj = models.Gacha(name=gacha['name'], image=gacha['image'], rarityPercent=gacha['rarityPercent'], description=gacha['description'])
        db.session.add(gacha_obj)
    db.session.commit()