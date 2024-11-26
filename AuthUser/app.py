import requests, time
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from datetime import datetime
import jwt
import scrypt
from python_json_config import ConfigBuilder
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{config.databases.auth.username}:{config.databases.auth.password}@{config.databases.auth.server}:{config.databases.auth.port}/{config.databases.auth.name}?driver=ODBC+Driver+17+for+SQL+Server'

for i in range(config.databases.retries):
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                            f'SERVER={config.databases.auth.server},{config.databases.auth.port};'
                            f'DATABASE=master;'
                            f'UID={config.databases.auth.username};'
                            f'PWD={config.databases.auth.password}')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{config.databases.auth.name}') \
        BEGIN CREATE DATABASE {config.databases.auth.name}; END")
        cursor.close()
        conn.close()
    except:
        time.sleep(config.databases.timeout)

db = SQLAlchemy(app)
import models
import AccountDBMethods
import AdminDBMethods

with app.app_context():
    db.create_all()

@app.route('/api/player/register', methods=['POST'])
def register_user():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data and 'profilePicture' in json_data:
        response = request.get(f'{config.dbmanagers.auth}/account/{json_data['username']}')
        if response.status_code == 200:
            return make_response(jsonify({"message":"Username taken."}, 409))
        salt = scrypt.gensalt()
        hashed_password=scrypt.hash(json_data['password'], salt)
        auth_data = {
            "username": json_data['username'],
            "password": hashed_password,
            "salt": salt
        }
        response = requests.post(f'{config.dbmanagers.auth}/account',  data=auth_data)
        if response.status == 200:
            userData = {
            'authId': response.get_json()['authId'],
            'ingameCurrency': 0,
            'profilePicture': json_data['profilePicture'],
            'registrationDate': datetime.now(),
            'status': "ACTIVE"}
            response = requests.post(f"{config.dbmanagers.user}/user", json=userData)
            return make_response(jsonify(response.get_json()), response.status)
        return make_response(jsonify({"message":"User registration failed."}), 400)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/login', methods=['POST'])
def login():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data:
        response = request.get(f'{config.dbmanagers.auth}/account/{json_data['username']}')
        if response.status_code == 404:
            response = request.get(f'{config.dbmanagers.auth}/account/{json_data['username']}')
            if response.status_code == 404:
                return make_response(jsonify({"message":"Username or password incorrect."}, 401))
        incoming_password=scrypt.hash(json_data['password'], response.json()['salt'])
        if incoming_password == response.json()['password']:
            token = 
            #check if a valid token is issued for the user; revoke it and make a mew one or return that token
            token_data ={
                "iss":"ASE Project",
                "exp":datetime.now()+datetime.timedelta(hours=5) ,
                "username":json_data['username'],
                "roles":"user"
            }
            jwt_encoded = jwt.encode(token_data, "secret", algorithm="HS256")
            #save the token to the database
            return make_response({"Access token":jwt_encoded}, 200)
        else:
            return make_response(jsonify({"message":"Username or password incorrect."}), 401)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/player/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization')
    
    if auth_header:
        parts = auth_header.split()
        
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            access_token = parts[1] 
        else:
            return jsonify({"error": "Invalid token format"}), 400
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(keycloak_url, headers=headers)
    if response.status_code == 200:
        print("User successfully logged out.")
    else:
        print(f"Error logging out: {response.status_code}")

def create_app():
    return app