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

"""GatchasUser ENDPOINTS"""

@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
def get_gacha_collection(userId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/player/gacha/player-collection/{userId}', headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(response.json(), response.status_code)

# Get player's gacha collection item
@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/player/gacha/player-collection/item/{collectionId}', headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(response.json(), response.status_code)

# Get player's gacha item details
@app.route('/api/player/gacha/player-collection/<int:userId>/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_gacha_details(userId, gachaId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/player/gacha/player-collection/{userId}/gacha/{gachaId}', headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(response.json(), response.status_code)

"""System Collection Endpoints"""

# Get full system gacha collection.
@app.route('/api/player/gacha/system-collection', methods=['GET'])
@handle_errors
def get_system_gacha_collection():
    response = requests.get(GACHA_MICROSERVICE + '/api/player/gacha/system-collection', headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(response.json(), response.status_code)

# Get details of a specific system gacha item.
@app.route('/api/player/gacha/system-collection/<int:gachaId>', methods=['GET'])
@handle_errors
def get_system_gacha_details(gachaId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/player/gacha/system-collection/{gachaId}', headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(response.json(), response.status_code)

"""Gacha Roll Endpoints"""
@app.route('/api/player/gacha/roll', methods=['POST'])
@handle_errors
def roll_gacha():
    response = requests.post(GACHA_MICROSERVICE + f'/api/player/gacha/roll', headers=request.headers, json=sanitize_data(request.get_json()), verify=False, timeout=config.timeout.high)
    return make_response(response.json(), response.status_code)

def create_app():
    return app

# Configuration for the database manager service
  # Replace with actual URL

@app.route('/api/player/currency<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    response = requests.get(config.services.paymentsmicroservice+f'/api/player/currency/transaction-history/{user_id}', headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(response.json()),response.status_code)


@app.route('/api/player/currency', methods=['POST'])
def purchase_in_game_currency():
    response = requests.post(f"{config.services.paymentsmicroservice}/api/player/currency/purchase", json=sanitize_data(request.get_json()), headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(response.json()),response.status_code)

@app.route('/api/player/decrease/<int:user_id>', methods=['PUT'])
def decrease_in_game_currency(user_id):
    response = requests.put(config.services.paymentsmicroservice+ f'/api/player/currency/decrease/{user_id}', json=sanitize_data(request.get_json()),  headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(response.json()),response.status_code)

@app.route('/api/player/increase/<int:user_id>', methods=['PUT'])
def increase_currency(user_id):
    response = requests.put(config.services.paymentsmicroservice+ f'/api/player/currency/increase/{user_id}', json=sanitize_data(request.get_json()), headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(response.json()),response.status_code) 

@app.route('/api/player/profile/<int:user_id>', methods=['GET'])
def getPlayerInformation(user_id):
    try:
        response = requests.get(f'{config.services.usersmicroservice}/api/player/profile/{user_id}',verify=False, timeout=config.timeout.medium)
        
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Player not found"}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": "Failed to connect to database API", "details": str(e)}), 500)

@app.route('/api/player/update/<int:user_id>', methods=['PUT'])
def updatePlayerInformation(user_id):
    response=requests.put(f'{config.services.usersmicroservice}/api/player/update/{user_id}',json=sanitize_data(request.get_json()),verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(response.json()),response.status_code)

@app.route('/api/player/delete/<int:user_id>', methods=['DELETE'])
def delete_player(user_id):
    delete_response = requests.delete(f'{config.services.usersmicroservice}/api/player/delete/{user_id}',verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(delete_response.json()),delete_response.status_code)
    
@app.route('/api/player/register', methods=['POST'])
def register_user():
    response = requests.post(f"{config.services.authmicroservice}/api/player/register", json=sanitize_data(request.get_json()), verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/player/login', methods=['POST'])
def user_login():
    response = requests.post(f"{config.services.authmicroservice}/api/player/login", json=sanitize_data(request.get_json()), verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/player/logout', methods=['POST'])
def user_logout():
    response = requests.post(f"{config.services.authmicroservice}/api/player/logout", headers=request.headers, verify=False, timeout=config.timeout.medium)
    return make_response(jsonify(response.json()), response.status_code)
