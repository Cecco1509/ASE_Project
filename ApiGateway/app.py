import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder
from handle_errors import handle_errors

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
AUCTION_ADMIN_URL = config.services.auctionsadmin
AUCTION_USER_URL = config.services.auctionsuser
GACHAS_ADMIN_URL = config.services.gachasadmin
GACHAS_USER_URL = config.services.gachasuser

"""AuctionsAdmin ENDPOINTS"""
@app.route('/api/admin/auction', methods=['GET'])
@handle_errors
def admin_auctions():
    """Fetch all auction items."""
    response = requests.get(AUCTION_ADMIN_URL + '/auction')
    response.raise_for_status()
    auction_items = response.json()
    return make_response(jsonify(auction_items), response.status_code)

@app.route('/api/admin/auction/<int:auctionId>', methods=['GET'])
@handle_errors
def get_single_auction(auctionId):
    """Fetch a single auction item by ID."""
    response = requests.get(AUCTION_ADMIN_URL + f'/auction/{auctionId}')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)
    
@app.route('/api/admin/auction/<int:auctionId>', methods=['PUT'])
@handle_errors
def modify_auction():
    """Create a new auction item."""
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    response = requests.post(AUCTION_ADMIN_URL + '/auction', json=json_data)
    
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/auction/<int:auctionId>', methods=['PUT'])
@handle_errors
def update_auction(auctionId):
    """Update a auction item."""
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    response = requests.put(AUCTION_ADMIN_URL + f'/auction/{auctionId}', json=json_data)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/auction/history', methods=['GET'])
@handle_errors
def auction_history():
    """GET auction history."""
    response = requests.get(AUCTION_ADMIN_URL + f'/auction/history')
    
    return make_response(jsonify(response.json()), response.status_code)

"""Fetch all auction user history."""
@app.route('/api/admin/auction/history/<int:userId>', methods=['GET'])
@handle_errors
def admin_auction_user_history(userId):
    response = requests.get(AUCTION_ADMIN_URL + '/history/{userId}')
    response.raise_for_status()
    auction_collections = response.json()
    return make_response(jsonify(auction_collections), response.status_code)


"""UserAuctions ENDPOINTS"""

@app.route('/api/player/auction/market', methods=['GET'])
@handle_errors
def auction_market():
    """GET auction history."""
    response = requests.get(AUCTION_USER_URL + f'/auction/history')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/player/auction', methods=['POST'])
@handle_errors
def create_auction():
    response = requests.post(AUCTION_USER_URL + f'/auction', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/player/auction/<auction_id>/bid', methods=['POST'])
def create_bid(auctionId):
    response = requests.post(AUCTION_USER_URL + f'/auction/{auctionId}/bid', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/player/auction/history', methods=['GET'])
def user_auction_history(auctionId):
    response = requests.post(AUCTION_USER_URL + f'/auction/history')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""GatchasAdmin ENDPOINTS"""
@app.route('/api/admin/gacha', methods=['GET'])
@handle_errors
def admin_gacha():
    """Fetch all gacha items."""
    response = requests.get(GACHAS_ADMIN_URL + '/api/admin/gacha')
    response.raise_for_status()
    gacha_items = response.json()
    return make_response(jsonify(gacha_items), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['GET'])
@handle_errors
def get_single_gacha(gachaId):
    """Fetch a single gacha item by ID."""
    response = requests.get(GACHAS_ADMIN_URL + f'/api/admin/gacha/{gachaId}')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)
    
@app.route('/api/admin/gacha', methods=['POST'])
@handle_errors
def create_gacha():
    """Create a new gacha item."""
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    response = requests.post(GACHAS_ADMIN_URL + '/api/admin/gacha', json=json_data)
    #response.raise_for_status()
    # i commented this line so the 400 error message will be returned the same, otherwise, the error message will be ovverriden
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['PUT'])
@handle_errors
def update_gacha(gachaId):
    """Update a gacha item."""
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    response = requests.put(GACHAS_ADMIN_URL + f'/api/admin/gacha/{gachaId}', json=json_data)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/gacha/<int:gachaId>', methods=['DELETE'])
@handle_errors
def delete_gacha(gachaId):
    """Delete a gacha item."""
    response = requests.delete(GACHAS_ADMIN_URL + f'/api/admin/gacha/{gachaId}')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)

"""Fetch all gacha collections."""
@app.route('/api/admin/gachacollection', methods=['GET'])
@handle_errors
def admin_gachacollection():
    response = requests.get(GACHAS_ADMIN_URL + '/api/admin/gachacollection')
    response.raise_for_status()
    gacha_collections = response.json()
    return make_response(jsonify(gacha_collections), response.status_code)

"""GatchasUser ENDPOINTS"""

@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
def get_gacha_collection(userId):
    response = requests.get(GACHAS_USER_URL + f'/api/player/gacha/player-collection/{userId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's gacha collection item
@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    response = requests.get(GACHAS_USER_URL + f'/api/player/gacha/player-collection/item/{collectionId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""System Collection Endpoints"""

# Get full system gacha collection.
@app.route('/api/player/gacha/system-collection', methods=['GET'])
@handle_errors
def get_system_gacha_collection():
    response = requests.get(GACHAS_USER_URL + '/api/player/gacha/system-collection')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get details of a specific system gacha item.
@app.route('/api/player/gacha/system-collection/<int:gachaId>', methods=['GET'])
@handle_errors
def get_system_gacha_details(gachaId):
    response = requests.get(GACHAS_USER_URL + f'/api/player/gacha/system-collection/{gachaId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""Gacha Roll Endpoints"""
@app.route('/api/player/gacha/roll', methods=['POST'])
@handle_errors
def roll_gacha():
    response = requests.post(GACHAS_USER_URL + f'/api/player/gacha/roll', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# TODO: create separate files and import them here

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

def create_app():
    return app
