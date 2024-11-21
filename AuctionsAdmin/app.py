import functools
import os
import threading
import requests, time
from python_json_config import ConfigBuilder

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ? 

def create_app():
    return app

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

print = functools.partial(print, flush=True)

def check_auction(auction) -> bool:
    if auction.auctionStart > auction.auctionEnd:
        return False
    
    collection = requests.get(config.dbmanagers.gacha+f"/gachacollection/{auction.gachaCollectionId}", verify=False)
    if collection.status_code != 200:
        return False
    
    return True


#GET /auctions: Admin view of all auctions.
@app.route('/auction', methods=['GET'])
def get_all_auctions():
    print(f"GET all auctions")
    try:
        response = requests.get(config.dbmanagers.auction + f'/auction', verify=False)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        auctions = response.json()
        return make_response(jsonify(auctions), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))

    
#GET /auction/<auctions_id>: Admin view specific auction.
@app.route('/auction/<int:auction_id>', methods=['GET'])
def get_auction(auction_id):
    print(f"GET auction", auction_id)
    try:
        response = requests.get(config.dbmanagers.auction + f'/auction/{auction_id}', verify=False)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        auction = response.json()
        return make_response(jsonify(auction), 200) ## Substitute with DBManager request,with BIDS
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
    

# PUT /api/admin/auction/{auction_id}: Modify a specific auction.
@app.route('/auction/<int:auction_id>', methods=['PUT'])
def update_auction(auction_id):
    print(f"PUT auction", auction_id)
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data:
            return make_response(jsonify({"message": "Invalid auction data"}), 400)
        
        # Validate auction data
        if not check_auction(data):  # Ensure check_auction is correct
            return make_response(jsonify({"message": "Invalid auction timestamps"}), 400)

        # Send PUT request to update the auction
        response = requests.put(
            f"{config.dbmanagers.auction}/auction/{auction_id}",
            json=data,
        )
        response.raise_for_status()  # Raise HTTPError for 4xx/5xx responses
        
        # Return success response
        return make_response(jsonify({"message": "Auction updated successfully"}), 200)
    except requests.exceptions.RequestException as e:
        print(f"External request failed: {e}")
        return make_response(jsonify({"message": "Failed to update auction", "error": str(e)}), 500)

    
# GET /api/admin/auction/history: Admin view of all market history (old auctions).
@app.route('/auction/history', methods=['GET'])
def history():
    print(f"GET Auctions History")
    try:

        response = requests.get(config.dbmanagers.auction + f'/auction/2')
        auctions = {"auctions" : []}

        if response.status_code != 404:
            auctions["auctions"] = response.json()

        return make_response(jsonify(auctions), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
    

@app.route('/auction/history/<user_id>', methods=['GET'])
def user_history(user_id):
    print(f"GET History of user " + user_id)
    try:
        data = request.get_json()

        auction = requests.get(config.dbmanagers.auction + f'/auction/user/{user_id}/2')

        return make_response(jsonify(auction.json()), 200) ## Substitute with DBManager request
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
