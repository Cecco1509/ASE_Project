import requests, time
from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder
from handle_errors import handle_errors
from utils import *


app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
GACHA_MICROSERVICE = config.services.gacha

"""GatchasAdmin ENDPOINTS"""
@app.route('/api/admin/gacha', methods=['GET'])
@handle_errors
def admin_gacha():
    response = requests.get(GACHA_MICROSERVICE + '/api/admin/gacha', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_single_gacha(gachaId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/admin/gacha/{gachaId}', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)
    
@app.route('/api/admin/gacha', methods=['POST'])
@handle_errors
def create_gacha():
    response = requests.post(GACHA_MICROSERVICE + '/api/admin/gacha', headers=request.headers, json=sanitize_data(request.get_json()), verify=False)
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['PUT'])
@handle_errors
def update_gacha(gachaId):
    response = requests.put(GACHA_MICROSERVICE + f'/api/admin/gacha/{gachaId}', headers=request.headers, json=sanitize_data(request.get_json()), verify=False)
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['DELETE'])
@handle_errors
def delete_gacha(gachaId):
    response = requests.delete(GACHA_MICROSERVICE + f'/api/admin/gacha/{gachaId}', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)

"""Fetch all gacha collections."""
@app.route('/api/admin/gachacollection', methods=['GET'])
@handle_errors
def admin_gachacollection():
    response = requests.get(GACHA_MICROSERVICE + '/api/admin/gachacollection', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)

def create_app():
    return app

@app.route('/api/admin/currency/<int:user_id>', methods=['GET'])
def get_transaction_history_admin(user_id):
    response = requests.get(config.services.paymentsmicroservice+f'/api/admin/currency/{user_id}', headers=request.headers, verify=False)
    return make_response(jsonify(response.json()),response.status_code)

@app.route('/api/admin/users', methods=['GET'])
def get_players():
    try:
        response = requests.get(f'{config.services.usersmicroservice}/api/admin/users',verify=False)
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Players not found"}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": "Failed to connect to database API", "details": str(e)}), 500)

@app.route('/api/admin/users/<int:user_id>', methods=['GET'])
def get_player(user_id):
    try:
        response = requests.get(f'{config.services.usersmicroservice}/api/admin/users/{user_id}',verify=False)
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Player not found"}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": "Failed to connect to database API", "details": str(e)}), 500)

@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def update_player(user_id):
    payload=request.get_json()
    response=requests.put(f'{config.services.usersmicroservice}/api/admin/users/{user_id}',json=payload,verify=False)
    return make_response(response.json(),response.status_code)


@app.route('/api/admin/users/ban/<int:user_id>', methods=['POST'])
def ban_player(user_id):
    response=requests.post(f'{config.services.usersmicroservice}/api/admin/users/ban/{user_id}',json=sanitize_data(request.get_json()),verify=False)
    return make_response(response.json(),response.status_code)

@app.route('/api/admin/register', methods=['POST'])
def register_admin():
    response = requests.post(f"{config.services.authmicroservice}/api/admin/register", json=sanitize_data(request.get_json()), verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    response = requests.post(f"{config.services.authmicroservice}/api/admin/login", json=sanitize_data(request.get_json()), verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    response = requests.post(f"{config.services.authmicroservice}/api/admin/logout", headers=request.headers, verify =False)
    return make_response(jsonify(response.json()), response.status_code)
