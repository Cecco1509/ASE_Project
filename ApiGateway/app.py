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
AUCTIONS_MICROSERVICE = config.services.auctionsservice
GACHA_MICROSERVICE = config.services.gacha

"""AuctionsAdmin ENDPOINTS"""

# GET /api/admin/auction: Admin view of all auctions.
@app.route('/api/admin/auction', methods=['GET'])
@handle_errors
def admin_auctions():
    """Fetch all auction items."""
    response = requests.get(AUCTIONS_MICROSERVICE + '/auction')
    response.raise_for_status()
    auction_items = response.json()
    return make_response(jsonify(auction_items), response.status_code)

# GET /api/admin/auction/{auction_id}: View specific auction details.
@app.route('/api/admin/auction/<int:auctionId>', methods=['GET'])
@handle_errors
def get_single_auction(auctionId):
    """Fetch a single auction item by ID."""
    response = requests.get(AUCTIONS_MICROSERVICE + f'/auction/{auctionId}')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)
    

# PUT /api/admin/auction/{auction_id}: Modify a specific auction.
@app.route('/api/admin/auction/<int:auctionId>', methods=['PUT'])
@handle_errors
def modify_auction(auctionId):
    """Modify a existent auction item."""

    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message": "No JSON data provided"}), 400)

    # External request to modify auction
    try:
        response = requests.put(
            f"{AUCTIONS_MICROSERVICE}/auction/{auctionId}",
            json=json_data,
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"message": "Failed to modify auction", "error": str(e)}), 500)

    # Return the response from the external service
    return make_response(jsonify(response.json()), response.status_code)

# GET /api/admin/auction/history: Admin view of all market history (old auctions)
@app.route('/api/admin/auction/history', methods=['GET'])
@handle_errors
def auction_history():
    """GET auction history."""
    try:
        # Make the external GET request
        response = requests.get(f"{AUCTIONS_MICROSERVICE}/auction/history")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        # Return the successful response to the client
        return make_response(jsonify(response.json()), response.status_code)

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve auction history: {e}")
        return make_response(jsonify({"message": "Failed to fetch auction history"}), 500)

# GET /api/admin/auction/history/{user_id}: Admin view of speceific user's market history (old auctions).
"""Fetch all auction user history."""
@app.route('/api/admin/auction/history/<int:userId>', methods=['GET'])
@handle_errors
def admin_auction_user_history(userId):
    response = requests.get(AUCTIONS_MICROSERVICE + '/history/{userId}')
    response.raise_for_status()
    auction_collections = response.json()
    return make_response(jsonify(auction_collections), response.status_code)


"""UserAuctions ENDPOINTS"""

# GET /api/player/auction/market: Get all active auctions in the market.
@app.route('/api/player/auction/market', methods=['GET'])
@handle_errors
def auction_market(userId):
    """GET auction history."""
    response = requests.get(AUCTIONS_MICROSERVICE + f'/auction/market')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)

# POST /api/player/auction/create: Create a new auction listing for a gacha item. (input: gacha id, bid min, timestamp, etc)
@app.route('/api/player/auction/create>', methods=['POST'])
@handle_errors
def create_auction():
    response = requests.post(AUCTIONS_MICROSERVICE + f'/auction/create', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# POST /api/player/auction/bid/{auction_id}: Place a bid on an active auction.
@app.route('/api/player/auction/bid/<auction_id>', methods=['POST'])
def create_bid(auctionId):
    response = requests.post(AUCTIONS_MICROSERVICE + f'/auction/{auctionId}/bid', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/player/auction/history', methods=['GET'])
def user_auction_history(auctionId):
    response = requests.post(AUCTIONS_MICROSERVICE + f'/auction/history')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

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
    response = requests.post(GACHA_MICROSERVICE + f'/api/player/gacha/roll', headers=request.headers, json=sanitize_data(request.get_json()), verify=False)
    return make_response(response.json(), response.status_code)

def create_app():
    return app

# Configuration for the database manager service
  # Replace with actual URL

@app.route('/api/player/currency<int:user_id>', methods=['GET'])
def get_transaction_history(user_id):
    response = requests.get(config.services.paymentsmicroservice+f'/api/player/currency/{user_id}', headers=request.headers, verify=False)
    return make_response(jsonify(response.json()),response.status_code)


@app.route('/api/player/currency/', methods=['POST'])
def purchase_in_game_currency():
    response = requests.post(f"{config.services.paymentsmicroservice}/api/player/currency/", json=sanitize_data(request.get_json()), headers=request.headers, verify=False)
    return make_response(jsonify(response.json()),response.status_code)

@app.route('/api/player/decrease/<int:user_id>', methods=['PUT'])
def decrease_in_game_currency(user_id):
    response = requests.put(config.services.paymentsmicroservice+ f'/api/player/decrease/update_balance', json=sanitize_data(request.get_json()),  headers=request.headers, verify=False)
    return make_response(jsonify(response.json()),response.status_code)

@app.route('/api/player/increase/<int:user_id>', methods=['PUT'])
def increase_currency(user_id):
    response = requests.put(config.services.paymentsmicroservice+ f'/api/player/increase/update_balance', json=sanitize_data(request.get_json()), headers=request.headers, verify=False)
    return make_response(jsonify(response.json()),response.status_code) 

@app.route('/api/admin/currency/<int:user_id>', methods=['GET'])
def get_transaction_history_admin(user_id):
    response = requests.get(config.services.paymentsmicroservice+f'/api/admin/currency/{user_id}', headers=request.headers, verify=False)
    return make_response(jsonify(response.json()),response.status_code)

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
    response=requests.put(f'{config.services.usersmicroservice}/api/player/update/{user_id}',json=sanitize_data(request.get_json()),verify=False)
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
    response=requests.post(f'{config.services.usersmicroservice}/api/admin/users/ban/{user_id}',json=sanitize_data(request.get_json()),verify=False)
    return make_response(response.json(),response.status_code)
    
@app.route('/api/player/register', methods=['POST'])
def register_user():
    response = requests.post(f"{config.services.authmicroservice}/api/player/register", json=sanitize_data(request.get_json()), verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/player/login', methods=['POST'])
def user_login():
    response = requests.post(f"{config.services.authmicroservice}/api/player/login", json=sanitize_data(request.get_json()), verify=False)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/player/logout', methods=['POST'])
def user_logout():
    response = requests.post(f"{config.services.authmicroservice}/api/player/logout", headers=request.headers, verify=False)
    return make_response(jsonify(response.json()), response.status_code)

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
