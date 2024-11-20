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
GACHA_ADMIN_URL = config.services.gachaadmin
GACHA_USER_URL = config.services.gachauser


"""GachasUser ENDPOINTS"""

@app.route('/api/player/gacha/player-collection/<int:userId>', methods=['GET'])
@handle_errors
def get_gacha_collection(userId):
    response = requests.get(GACHA_USER_URL + f'/api/player/gacha/player-collection/{userId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's gacha collection item
@app.route('/api/player/gacha/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_gacha_collection_details(collectionId):
    response = requests.get(GACHA_USER_URL + f'/api/player/gacha/player-collection/item/{collectionId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""System Collection Endpoints"""

# Get full system gacha collection.
@app.route('/api/player/gacha/system-collection', methods=['GET'])
@handle_errors
def get_system_gacha_collection():
    response = requests.get(GACHA_USER_URL + '/api/player/gacha/system-collection')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get details of a specific system gacha item.
@app.route('/api/player/gacha/system-collection/<int:gachaId>', methods=['GET'])
@handle_errors
def get_system_gacha_details(gachaId):
    response = requests.get(GACHA_USER_URL + f'/api/player/gacha/system-collection/{gachaId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""gacha Roll Endpoints"""
@app.route('/api/player/gacha/roll', methods=['POST'])
@handle_errors
def roll_gacha():
    response = requests.post(GACHA_USER_URL + f'/api/player/gacha/roll', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# TODO: create separate files and import them here





































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
    response = requests.post(GACHA_USER_URL + f'/auction', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/player/auction/<auction_id>/bid', methods=['POST'])
def create_bid(auctionId):
    response = requests.post(GACHA_USER_URL + f'/auction/{auctionId}/bid', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

@app.route('/api/player/auction/history', methods=['GET'])
def user_auction_history(auctionId):
    response = requests.post(GACHA_USER_URL + f'/auction/history')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

def create_app():
    return app