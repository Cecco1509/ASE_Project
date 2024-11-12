import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from datetime import datetime
from python_json_config import ConfigBuilder

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('./config.json')

@app.route('/api/player/register', methods=['POST'])
def register_user():
    json_data = request.get_json()
    if json_data |json_data['username'] | json_data['password']:
        user = request.get(f"{config.db_manager_url}/account/username/{json_data['username']}")
        if user:
            return make_response(jsonify({"message":"Username taken."}), 400)
        authData = {"username":json_data['username'],"password":json_data['password']}
        response = requests.post(f"{config.db_manager_url}/account", json=authData)
        if response.status == 200:
            userData = {
            'authId': response.get_json()['authId'],
            'ingameCurrency': 0,
            'profilePicture': json_data['profilePicture'],
            'registrationDate': datetime.now(),
            'status': "ACTIVE"}
            response = requests.post(f"{config.db_manager_url}/user", json=userData)
            return make_response(jsonify(response.get_json()), response.status)
        return make_response(jsonify({"message":"User registration failed."}), 400)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('/api/player/login/<int:userId>', methods=['POST'])
def login(userId):
    json_data = request.get_json()
    if json_data:
        response = requests.get(f"{config.db_manager_url}/user/{userId}")
        response_json = response.get_json()
        if response.status == 200:
            if json_data['username'] == response_json['username'] & json_data['password']==response_json['password']:
                return make_response({"message":"User succesfully loged in."}, 200)
            return make_response(jsonify({"message":"Username or password incorrect."}), 400)
    return make_response(jsonify({"message":"Invalid data."}), 400)

@app.route('api/player/logout/<int:userId>', method=['POST'])
def logout(userId):
    return make_response({"message":"User succuesfully logged out."}, 200)

def create_app():
    return app