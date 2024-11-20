import requests, time

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from python_json_config import ConfigBuilder
from handle_errors import handle_errors

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')
AUCTION_ADMIN_URL = config.services.auctionadmin
AUCTION_USER_URL = config.services.auctionuser

"""AuctionssAdmin ENDPOINTS"""
@app.route('/api/admin/auction', methods=['GET'])
@handle_errors
def admin_auctions():
    """Fetch all auction items."""
    response = requests.get(AUCTION_ADMIN_URL + '/api/admin/auction')
    response.raise_for_status()
    auction_items = response.json()
    return make_response(jsonify(auction_items), response.status_code)

@app.route('/api/admin/auction/<int:auctionId>', methods=['GET'])
@handle_errors
def get_single_auction(auctionId):
    """Fetch a single auction item by ID."""
    response = requests.get(AUCTION_ADMIN_URL + f'/api/admin/auction/{auctionId}')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)
    
@app.route('/api/admin/auction/<int:auctionId>', methods=['PUT'])
@handle_errors
def create_auction():
    """Create a new auction item."""
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    response = requests.post(AUCTION_ADMIN_URL + '/api/admin/auction', json=json_data)
    #response.raise_for_status()
    # i commented this line so the 400 error message will be returned the same, otherwise, the error message will be ovverriden
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/auction/<int:auctionId>', methods=['PUT'])
@handle_errors
def update_auction(auctionId):
    """Update a auction item."""
    json_data = request.get_json()

    if not json_data:
        return make_response(jsonify({"message":"No JSON data provided"}), 400)

    response = requests.put(AUCTION_ADMIN_URL + f'/api/admin/auction/{auctionId}', json=json_data)
    return make_response(jsonify(response.json()), response.status_code)

@app.route('/api/admin/auction/history', methods=['GET'])
@handle_errors
def auction_history():
    """GET auction history."""
    response = requests.get(AUCTION_ADMIN_URL + f'/api/admin/auction/history')
    response.raise_for_status()
    return make_response(jsonify(response.json()), response.status_code)

"""Fetch all auction collections."""
@app.route('/api/admin/auction/history/<int:userId>', methods=['GET'])
@handle_errors
def admin_auction_user_history(userId):
    response = requests.get(AUCTION_ADMIN_URL + '/api/admin/history/{userId}')
    response.raise_for_status()
    auction_collections = response.json()
    return make_response(jsonify(auction_collections), response.status_code)

"""AuctionsUser ENDPOINTS"""

@app.route('/api/player/auction/player-collection/<int:userId>', methods=['GET'])
@handle_errors
def get_auction_collection(userId):
    response = requests.get(AUCTION_USER_URL + f'/api/player/auction/player-collection/{userId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get player's auction collection item
@app.route('/api/player/auction/player-collection/item/<int:collectionId>', methods=['GET'])
@handle_errors
def get_auction_collection_details(collectionId):
    response = requests.get(AUCTION_USER_URL + f'/api/player/auction/player-collection/item/{collectionId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""System Collection Endpoints"""

# Get full system auction collection.
@app.route('/api/player/auction/system-collection', methods=['GET'])
@handle_errors
def get_system_auction_collection():
    response = requests.get(AUCTION_USER_URL + '/api/player/auction/system-collection')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# Get details of a specific system auction item.
@app.route('/api/player/auction/system-collection/<int:auctionId>', methods=['GET'])
@handle_errors
def get_system_auction_details(auctionId):
    response = requests.get(AUCTION_USER_URL + f'/api/player/auction/system-collection/{auctionId}')
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

"""auction Roll Endpoints"""
@app.route('/api/player/auction/roll', methods=['POST'])
@handle_errors
def roll_auction():
    response = requests.post(AUCTION_USER_URL + f'/api/player/auction/roll', json=request.get_json())
    response.raise_for_status()
    return make_response(response.json(), response.status_code)

# TODO: create separate files and import them here

def create_app():
    return app