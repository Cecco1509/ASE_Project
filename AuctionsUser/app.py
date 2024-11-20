import functools
import os
import threading
import requests, time
from flask import jsonify
from python_json_config import ConfigBuilder

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ?

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

# GET /api/player/auction/market: Get all active auctions in the market.
@app.route('/auction/market', methods=['GET'])
def get_auctions():
    try:
        response = requests.get(config.dbmanagers.auction + '/auction/1')
        response.raise_for_status()
        return make_response(jsonify(market=response.json()), 200)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}, 500))
    

#POST /api/player/auction/create: Create a new auction listing for a gacha item. (input: gacha id, bid min, timestamp, etc)
@app.route('/auction/create', methods=['POST'])
def create_auction():
    try:
        data = request.get_json()
        response = requests.post(config.dbmanagers.auction + '/auction', json=data)
        response.raise_for_status()
        return make_response(jsonify(auction=response.json()), 201)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)
    
#POST /api/player/auction/{auction_id}/bid: Place a bid on an active auction.
@app.route('/auction/<auction_id>/bid', methods=['POST'])
def bid_on_auction(auction_id):
    try:
        data = request.get_json()
        response = requests.post(config.dbmanagers.auction + f'/auction/{auction_id}/bid', json=data.bid)
        response.raise_for_status()
        return make_response(jsonify({"message": "Bid done"}), 201)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)
    

    ## TOKENS DA INSERIRE
@app.route('/auction/history', methods=['POST'])
def auction_player_history():
    try:
        data = request.get_json()
        response = requests.post(config.dbmanagers.auction + f'/auction/{DAINSERIRE}/2', json=data.bid)
        response.raise_for_status() #/auction/<int:userId>/<string:status>
        return make_response(response.json(), 200)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)

def create_app():
    return app
