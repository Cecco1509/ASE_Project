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
    

@app.route('/auction/<int:auction_id>', methods=['PUT'])
def update_auction(auction_id):
    print(f"PATCH auction", auction_id)
    try:
        try:
            data = request.get_json()
        except Exception as e:
            print(f"ERROR -> ", e)
            return make_response(jsonify({"message": "Invalid auction data"}), 400)
        
        if (not check_auction(data)):
            return make_response(jsonify({"message": "Invalid auction data"}), 400)

        response = requests.put(config.dbmanagers.auction + f'/auction/{auction_id}', json=data.to_dict(), headers={
            "Content-Type": "application/json",
        })
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        #response.json()
        return make_response(jsonify({"message" : "Correctly updated"}), 200) ## Substitute with DBManager request
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
    

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
        auction = data

        user_collection_res = requests.get(config.dbmanagers.gacha + f'/gachacollection/{user_id}')

        auction_req = requests.get(config.dbmanagers.auction + '/auction')

        user_collection = user_collection_res.json()
        auctions = auction_req.json()

        if user_collection is None:
            user_collection = {}

        if auctions is None:
            auctions = {}

        history = {}

        return make_response(jsonify({"history":jsonify(history), "usercoll":user_collection, "auctions": auctions}), 200) ## Substitute with DBManager request
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
