import requests, time
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from datetime import datetime, timedelta, timezone
import jwt
from python_json_config import ConfigBuilder
from functools import *
import os
import json
from flask_bcrypt import Bcrypt
from authdb_mock import *
from dotenv import load_dotenv

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
load_dotenv()
app.config['SECRET_KEY']=str(os.getenv("SECRET_KEY"))

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
        response = get_user(json_data['username'])
        if response != None:
            return make_response(jsonify({"message":"Username taken."}), 409)
        salt = get_salt()
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
            response = create_user(userData)
            return make_response(jsonify({"userId":response['userId']}), 200)
        return make_response(jsonify({"message":"User registration failed."}), 400)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/player/login', methods=['POST'])
def login():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data:
        response = get_user(json_data['username'])
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
            return make_response(jsonify({"message":f"Username or password incorrect. {response['password']}, {salt}"}), 401)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/player/logout', methods=['POST'])
@token_required("player")
def logout(user_info):
    token = valid_tokens.pop(user_info['username'])
    if token:
        return make_response(jsonify({"message":"User succesfully logged out."}),200)
    return make_response(jsonify({"message":"Error while log out."}),400)

@app.route('/api/player/UserInfo', methods=['GET'])
@token_required("player")
def user_info(user_info):
    response = get_user_info(user_info['userId'])
    if response:
        return make_response(jsonify(response),200)
    return make_response(jsonify({"message":"User not found."}),404)

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
        response = get_user(json_data['username'])
        if response != None:
            return make_response(jsonify({"message":"Username taken."}), 409)
        salt = get_salt()
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
        response =  get_user(json_data['username'])
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