import collections
from datetime import datetime
import functools
import os
import threading
import sys
import requests, time
from flask import jsonify
from celery import Celery
from python_json_config import ConfigBuilder

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ?

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

sys.path.append("/app/")  
from celery_app import end_auction

# celery_app = Celery(app.name,
#                     broker='amap://admin:mypass@rabbit:5672', 
#                     backend='rpc://')

# GET /api/player/auction/market: Get all active auctions in the market.


############################################################# USER ##########################################################

@app.route('/auction/market', methods=['GET'])
def get_auctions():
    try:
        response = requests.get(config.dbmanagers.auction + '/auction/status/1')
        response.raise_for_status()
        return make_response(jsonify(market=response.json()), 200)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}, 500))
    

#POST /api/player/auction/create: Create a new auction listing for a gacha item. (input: gacha id, bid min, timestamp, etc)
@app.route('/auction/create', methods=['POST'])
def create_auction():
    try:
        data = request.get_json()
        if (not 'gachaCollectionId' in data or
            not 'userId'  in data or
            not 'auctionStart' in data or
            not 'auctionEnd' in data or
            not 'minimumBid' in data or
            not 'status' in data) :

            return make_response(jsonify({"message": "Invalid data"}), 400);
    
        start = datetime.strptime(data['auctionStart'], '%Y-%m-%dT%H:%M:%SZ')
        end = datetime.strptime(data['auctionEnd'], '%Y-%m-%dT%H:%M:%SZ')
        now = datetime.now();

        if (start < now or end < now or start > end):
            return make_response(jsonify({"message": "Auction start or end time must be in the future"}), 400);
        
        active_auction = request.get(config.dbmanagers.auction + f'/auction/user/{data["userId"]}/{data["gachaCollectionId"]}/1')
        if active_auction.status_code == 200:
            return make_response(jsonify({"message": f"User {data['userId']} already has an active auction for that"}), 400);
    
        response = requests.post(config.dbmanagers.auction + '/auction', json=data)
        new_auction = response.json().get('auctionId');

        r = end_auction.apply_sync(args=('auctionId',new_auction), eta=end);

        return make_response(jsonify(auction=response.json()), 201)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)
    
#POST /api/player/auction/{auction_id}/bid: Place a bid on an active auction.
@app.route('/auction/<auction_id>/bid', methods=['POST']) ## {userID, amount}
def bid_on_auction(auction_id):
    try:
        data = request.get_json()
        response = requests.post(config.dbmanagers.auction + f'/auction/{auction_id}/bid', json=data.bid)
        ### Remove previous bid
        
        user_bids = requests.get(config.dbmanagers.auction + f'/auctionbid/user/{data["userId"]}/{auction_id}')
        auction_bids = requests.get(config.dbmanagers.auction + f'/auctionbid/{auction_id}')
        userBidId = None
        userBidAmount = 0
        if (user_bids.status_code == 200):
            for bid in user_bids.json():
                userBidId = bid['bidId']

        auctionBidAmount = 0
        if (auction_bids.status_code == 200):
            for bid in auction_bids.json():
                if bid['bidAmount'] > auctionBidAmount:
                    auctionBidAmount = bid['bidAmount']

        if auctionBidAmount > data["bidAmount"]: return make_response(jsonify({"message": "Bid Amount inferior of previous one"}), 201)

        requests.post(config.dbmanagers.auction + f'/auctionbid', json=jsonify({'userId': data["userId"], 'bidAmount': data["bidAmount"], 'auctionId':auction_id, 'timestamp':datetime.now()}),)

        resp = requests.put(
                f"{config.services.paymentsuser}/api/player/currency/decrese/{bid['userId']}",
                json={"amount": bid['bidAmount']}
            )
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
    


def check_auction(auction) -> bool:
    if auction.auctionStart > auction.auctionEnd:
        return False
    
    collection = requests.get(config.dbmanagers.gacha+f"/gachacollection/{auction.gachaCollectionId}", verify=False)
    if collection.status_code != 200:
        return False
    
    return True

##################################################### ADMIN ############################################################

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


def create_app():
    return app
