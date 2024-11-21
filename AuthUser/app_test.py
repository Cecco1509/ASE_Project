import requests, time

from flask import Flask, request, make_response, jsonify 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from datetime import datetime
from python_json_config import ConfigBuilder
from authdb_mock import *

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

@app.route('/api/player/register', methods=['POST'])
def register_user():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data and 'profilePicture'  in json_data:
        user = get_user(json_data['username'])
        if user:
            return make_response(jsonify({"message":"Username taken."}), 409)
        authData = {"username":json_data['username'],"password":json_data['password']}
        response = create_account(authData)
        if response['status'] == 200:
            userData = {
            'authId': response['data'],
            'ingameCurrency': 0,
            'profilePicture': json_data['profilePicture'],
            'registrationDate': datetime.now(),
            'status': "ACTIVE"}
            response = create_user(userData)
            return make_response(jsonify({"userId":response['data']}), response['status'])
        return make_response(jsonify({"message":"User registration failed."}), 400)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/player/login', methods=['POST'])
def login():
    json_data = request.get_json()
    if json_data and 'username' in json_data and 'password' in json_data:
        response = get_user(json_data['username'])
        response_json = response["data"]
        if response['status'] == 200:
            if json_data['username'] == response_json['username'] and json_data['password']==response_json['password']:
                return make_response({"message":"User succesfully logged in."}, 200)
        return make_response(jsonify({"message":"Username or password incorrect."}), 400)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/player/logout/<int:userId>', methods=['POST'])
def logout(userId):
    return make_response({"message":"User succuesfully logged out."}, 200)

def create_app():
    return app