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
    sanitized_data = sanitize_data(request.get_json())
    response = requests.post(GACHA_MICROSERVICE + '/api/admin/gacha', headers=request.headers, json=sanitized_data, verify=False)
    return make_response(response.json(), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['PUT'])
@handle_errors
def update_gacha(gachaId):
    sanitized_data = sanitize_data(request.get_json())
    response = requests.put(GACHA_MICROSERVICE + f'/api/admin/gacha/{gachaId}', headers=request.headers, json=sanitized_data, verify=False)
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

"""GatchasUser ENDPOINTS"""

@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
def get_gacha_collection(userId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/player/gacha/player-collection/{userId}', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)

# Get player's gacha collection item
@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/player/gacha/player-collection/item/{collectionId}', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)

# Get player's gacha item details
@app.route('/api/player/gacha/player-collection/<int:userId>/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_gacha_details(userId, gachaId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/player/gacha/player-collection/{userId}/gacha/{gachaId}', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)

"""System Collection Endpoints"""

# Get full system gacha collection.
@app.route('/api/player/gacha/system-collection', methods=['GET'])
@handle_errors
def get_system_gacha_collection():
    response = requests.get(GACHA_MICROSERVICE + '/api/player/gacha/system-collection', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)

# Get details of a specific system gacha item.
@app.route('/api/player/gacha/system-collection/<int:gachaId>', methods=['GET'])
@handle_errors
def get_system_gacha_details(gachaId):
    response = requests.get(GACHA_MICROSERVICE + f'/api/player/gacha/system-collection/{gachaId}', headers=request.headers, verify=False)
    return make_response(response.json(), response.status_code)

"""Gacha Roll Endpoints"""
@app.route('/api/player/gacha/roll', methods=['POST'])
@handle_errors
def roll_gacha():
    response = requests.post(GACHA_MICROSERVICE + f'/api/player/gacha/roll', headers=request.headers, json=request.get_json(), verify=False)
    return make_response(response.json(), response.status_code)

def create_app():
    return app

# Configuration for the database manager service
  # Replace with actual URL

@app.route('/api/player/currency<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    
        # Send a GET request to the database manager service to fetch transaction history
        response = requests.get(config.services.payments_player_microservice+f'/api/player/currency/{user_id}')
        return response


@app.route('/api/player/currency/', methods=['POST'])
def purchase_in_game_currency():
        # Prepare payload
        data = request.get_json()
        # Send request to microservice
        response = requests.post(f"{config.services.payments_player_microservice}/api/player/currency/", json=data)
        # Forward the microservice's response to the user
        return response

@app.route('/api/player/decrease/<int:user_id>', methods=['PUT'])
def decrease_in_game_currency(user_id):
    
        # Extract the amount to be deducted from the request body
        data = request.get_json()
        
        response = requests.put(config.services.payments_player_microservice+ f'/api/player/decrease/update_balance', json=data)
        
        return response


@app.route('/api/player/increase/<int:user_id>', methods=['PUT'])
def increase_currency(user_id):
    
        data = request.get_json()
        
        response = requests.put(config.services.payments_player_microservice+ f'/api/player/increase/update_balance', json=data)

        return response

   

@app.route('/api/admin/currency/<int:user_id>', methods=['GET'])
def get_admin_transaction_history(user_id):
    
        response = requests.get(config.services.paymentsadmin+f'/api/admin/currency/{user_id}')
        return response

       


@app.route('/api/player/profile/<int:user_id>', methods=['GET'])
def getPlayerInformation(user_id):
    try:
        response = requests.get(f'{config.services.usersmicroservice}/api/player/profile/{user_id}',verify=False)
        
        if response.status_code == 200:
            return make_response(jsonify(response.json()), 200)
        else:
            return make_response(jsonify({"error": "Player not found"}), response.status_code)
    except requests.RequestException as e:
        return make_response(jsonify({"error": "Failed to connect to database API", "details": str(e)}), 500)

@app.route('/api/player/update/<int:user_id>', methods=['PUT'])
def updatePlayerInformation(user_id):
    payload=request.get_json()
    response=requests.put(f'{config.services.usersmicroservice}/api/player/update/{user_id}',json=payload,verify=False)
    return make_response(jsonify(response.json()),response.status_code)

@app.route('/api/player/delete/<int:user_id>', methods=['DELETE'])
def delete_player(user_id):
    delete_response = requests.delete(f'{config.services.usersmicroservice}/api/player/delete/{user_id}',verify=False)
    return make_response(jsonify(delete_response.json()),delete_response.status_code)
    



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
    payload=request.get_json()
    response=requests.post(f'{config.services.usersmicroservice}/api/admin/users/ban/{user_id}',json=payload,verify=False)
    return make_response(response.json(),response.status_code)
    
@app.route('/api/player/register', methods=['POST'])
def register_user():
    response = requests.post(f"{config.services.authmicroservice}/api/player/register", json=request.get_json(), verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/player/login', methods=['POST'])
def user_login():
    response = requests.post(f"{config.services.authmicroservice}/api/player/login", json=request.get_json(), verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/player/logout', methods=['POST'])
def user_logout():
    response = requests.post(f"{config.services.authmicroservice}/api/player/logout", headers=request.headers, verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/register', methods=['POST'])
def register_admin():
    response = requests.post(f"{config.services.authmicroservice}/api/admin/register", json=request.get_json(), verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    response = requests.post(f"{config.services.authmicroservice}/api/admin/login", json=request.get_json(), verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    response = requests.post(f"{config.services.authmicroservice}/api/admin/logout", headers=request.headers, verify =False)
    return make_response(jsonify(response.json()), response.status_code)
