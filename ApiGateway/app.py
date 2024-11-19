import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

@app.route('/api/player/register', methods=['POST'])
def register_user():
    return request.post(f"{config.services.authuser}/api/player/register", json=request.get_json())

@app.route('/api/player/login', methods=['POST'])
def login(userId):
    return request.post(f"{config.services.authuser}/api/player/login", json=request.get_josn())

@app.route('api/player/logout/<int:userId>', method=['POST'])
def logout(userId):
    return request.post(f"{config.services.authuser}/api/player/logout/{userId}")

def create_app():
    return app