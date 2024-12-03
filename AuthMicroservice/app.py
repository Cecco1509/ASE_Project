import requests, time
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from datetime import datetime, timedelta, timezone
import jwt
from python_json_config import ConfigBuilder
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from functools import *
import os
import json
from flask_bcrypt import Bcrypt 
from dotenv import load_dotenv

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 
load_dotenv()
app.config['SECRET_KEY']=str(os.getenv("SECRET_KEY"))

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

with open('/run/secrets/db_password', 'r') as file:
    password = file.read().strip()

app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{config.databases.auth.username}:{password}@{config.databases.auth.server}:{config.databases.auth.port}/{config.databases.auth.name}?driver=ODBC+Driver+17+for+SQL+Server'

for i in range(config.databases.retries):
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                            f'SERVER={config.databases.auth.server},{config.databases.auth.port};'
                            f'DATABASE=master;'
                            f'UID={config.databases.auth.username};'
                            f'PWD={password};'
                            'Encrypt=yes;TrustServerCertificate=yes')
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
from AccountDBMethods import *
from AdminDBMethods import *

with app.app_context():
    db.create_all()

valid_tokens = dict()
bcrypt = Bcrypt(app)

def parse_json(data):
    return json.loads(json.dumps(data))

def token_required(role=None):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):

            ## Read the token from authorization header
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({'message':'Token is missing!'}), 401
            token = request.headers.get('Authorization').split(' ')[1]
            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], "HS256")
                expiration_str = data['exp_time']
                if expiration_str:
                    expiration = datetime.fromisoformat(expiration_str)
                    if expiration < datetime.now(timezone.utc):
                        return jsonify({'message': 'Token has expired!'}), 403
                    
                if role and str(data['roles']) != role:
                    return jsonify({'message': 'Unauthorized role!'}), 403
                
                valid_token = valid_tokens.get(data['username'])
                if not valid_token:
                    return jsonify({'message':'Invalid token!'}),403
                user = {"username":data['username'],"userId":data['userId'], "role":data['roles'], "token":token}

            except Exception as e:
                print('Error decoding token: ', str(e))
                return jsonify({'message': 'Invalid token', 'error': str(e)}), 403

            return func(*args, **kwargs, user_info=parse_json(user))

        return decorated
    return decorator

@app.route('/api/player/register', methods=['POST'])
def register_user():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data and 'profilePicture' in json_data:
        response = get_account_by_username(json_data['username'])
        if response != None:
            return make_response(jsonify({"message":"Username taken."}, 409))
        salt = os.urandom(32)
        hashed_password=bcrypt.generate_password_hash(json_data['password']).decode('utf-8') 
        auth_data = {
            'username': json_data['username'],
            'password': hashed_password,
            'salt': salt
        }
        response = create_account(auth_data)
        if response != None:
            userData = {
            'authId': response['accountId'],
            'ingameCurrency': 0,
            'profilePicture': json_data['profilePicture'],
            'registrationDate': datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
            'status': "ACTIVE"}
            response = requests.post(f'{config.dbmanagers.user}/user', json=userData, verify=False)
            if response.status_code==200:
                return make_response(jsonify(response.json()), response.status_code)
        return make_response(jsonify({"message":"User registration failed."}), 400)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/player/login', methods=['POST'])
def login():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data:
        response = get_account_by_username(json_data['username'])
        if response==None:
            return make_response(jsonify({"message":"Username or password incorrect."}), 401)
        role ="player"
        if bcrypt.check_password_hash(response['password'], json_data['password']):
            token_data ={
                "iss":"ASE Project",
                "exp_time":str(datetime.now(timezone.utc)+timedelta(hours=5)) ,
                "username":json_data['username'],
                "roles":role,
                "userId":response['id']
            }
            jwt_encoded = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm="HS256")
            valid_tokens[json_data['username']]=jwt_encoded
            return make_response({"Access token":jwt_encoded}, 200)
        else:
            return make_response(jsonify({"message":f"Username or password incorrect."}), 401)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/player/logout', methods=['POST'])
@token_required("player")
def logout(user_info):
    token = valid_tokens.pop(user_info['username'])
    if token:
        return make_response(jsonify({"message":"User succesfully logged out."}),200)
    return make_response(jsonify({"message":"Error while log out."}),400)

@app.route('/api/player/UserInfo', methods=['POST'])
@token_required("player")
def userInfo(user_info):
    response = requests.post(f'{config.dbmanagers.user}/user/auth/{user_info['userId']}', verify=False)
    if response.status_code==200:
        return make_response(jsonify(response.json()),200)
    return make_response(jsonify(response.json()),response.status_code)

@app.route('/helloPlayer', methods=['GET'])
@token_required("player")
def verify_player_token(user_info=None):
    try:
        return make_response(jsonify({"userId" : user_info['userId']}), 200)
    except Exception as e:
        return make_response(jsonify({"error" : str(e)}), 500)
 
@app.route('/helloAdmin', methods=['GET'])
@token_required("admin")
def verify_admin_token(user_info=None):
    try:
        return make_response(jsonify({"adminId" : user_info['userId']}), 200)
    except Exception as e:
        return make_response(jsonify({"error" : str(e)}), 500)

@app.route('/api/admin/register', methods=['POST'])
def register_admin():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data:
        response = get_admin_by_username(json_data['username'])
        if response != None:
            return make_response(jsonify({"message":"Username taken."}), 409)
        salt = os.urandom(32)
        hashed_password=bcrypt.generate_password_hash(json_data['password']).decode('utf-8') 
        auth_data = {
            'username': json_data['username'],
            'password': hashed_password,
            'salt': salt
        }
        response = create_admin(auth_data)
        if response != None:
                return make_response(jsonify(response), 200)
        return make_response(jsonify({"message":"Admin registration failed."}), 400)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data:
        response = get_admin_by_username(json_data['username'])
        if response==None:
            return make_response(jsonify({"message":"Username or password incorrect."}), 401)
        role = "admin"
        if bcrypt.check_password_hash(response['password'], json_data['password']):
            token_data ={
                "iss":"ASE Project",
                "exp_time":str(datetime.now(timezone.utc)+timedelta(hours=5)) ,
                "username":json_data['username'],
                "roles":role,
                "userId":response['id']
            }
            jwt_encoded = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm="HS256")
            valid_tokens[json_data['username']]=jwt_encoded
            return make_response({"Access token":jwt_encoded}, 200)
        else:
            return make_response(jsonify({"message":f"Username or password incorrect."}), 401)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/admin/logout', methods=['POST'])
@token_required("admin")
def admin_logout(user_info):
    token = valid_tokens.pop(user_info['username'])
    if token:
        return make_response(jsonify({"message":"Admin succesfully logged out."}),200)
    return make_response(jsonify({"message":"Error while log out."}),400)
