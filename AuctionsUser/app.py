import collections
from datetime import datetime
import functools
import os
import threading
import requests, time
from flask import jsonify
from celery import Celery
from python_json_config import ConfigBuilder

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from celery_app import end_auction

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ?

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

# celery_app = Celery(app.name,
#                     broker='amap://admin:mypass@rabbit:5672', 
#                     backend='rpc://')

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
@app.route('/auction/create/<int:userId>', methods=['POST'])
def create_auction(userId):
    try:
        data = request.get_json()
        if (not 'gachaCollectionId' in data or
            not 'userId'  in data or
            not 'auctionStart' in data or
            not 'auctionEnd' in data or
            not 'minimumBid' in data) :

            return make_response(jsonify({"message": "Invalid data"}), 400);
    
        start = datetime.strptime(data['auctionStart'], '%Y-%m-%dT%H:%M:%SZ')
        end = datetime.strptime(data['auctionEnd'], '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.now();

        if (start < now or end < now or start > end):
            return make_response(jsonify({"message": "Auction start or end time must be in the future"}), 400);
        
        active_auction = request.get(config.dbmanagers.auction + f'/auction/user/{userId}/{data["gachaCollectionId"]}/1')
        if active_auction.status_code == 200:
            return make_response(jsonify({"message": f"User {userId} already has an active auction for that"}), 400);
    
        response = requests.post(config.dbmanagers.auction + '/auction', json=data)
        new_auction = response.json().get('auctionId');

        r = end_auction.apply_sync(args=('auctionId',new_auction), eta=end);

        return make_response(jsonify(auction=response.json()), 201)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)
    
#POST /api/player/auction/{auction_id}/bid: Place a bid on an active auction.
@app.route('/auction/<auction_id>/bid', methods=['POST'])
def bid_on_auction(auction_id):
    try:
        data = request.get_json()
        response = requests.post(config.dbmanagers.auction + f'/auction/{auction_id}/bid', json=data.bid)
        ### Remove previous bid
        ### Decrease money amount
        response.raise_for_status()
        return make_response(jsonify({"message": "Bid done"}), 201)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)
    

    ## TOKENS DA INSERIRE
@app.route('/auction/history/<int:userId>', methods=['GET'])
def auction_player_history(userId):
    try:
        data = request.get_json()
        response = requests.get(config.dbmanagers.auction + f'/auction/{userId}/2')
        return make_response(response.json(), 200)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)

def create_app():
    return app
