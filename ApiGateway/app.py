import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

user_microservice_url = "usersuser:5000"

@app.route('/api/player/register', methods=['POST'])
def register_user():
    return request.post(f"{user_microservice_url}/api/player/register", payload=request.get_json())

@app.route('/api/player/login/<int:userId>', methods=['POST'])
def login(userId):
    return request.post(f"{user_microservice_url}/api/player/login/{userId}")

@app.route('api/player/logout/<int:userId>', method=['POST'])
def logout(userId):
    return request.post(f"{user_microservice_url}/api/player/logout/{userId}")

def create_app():
    return app