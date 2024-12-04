import collections
from datetime import datetime
import functools
from numbers import Number
import os
import threading
import sys
import requests, time
from flask import jsonify
from python_json_config import ConfigBuilder
import pytz
from celery import Celery

from flask import Flask, request, make_response, jsonify
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound
from auth_utils import *
from handle_errors import *

app = Flask(__name__, instance_relative_config=True) #instance_relative_config=True ?

builder = ConfigBuilder()
config = builder.parse_config('/app/config.json')

celery_app = Celery('worker',
                broker='amqp://admin:mypass@rabbit:5672', 
                backend='rpc://')

############################################################# USER ##########################################################

@app.route('/player/auction/market', methods=['GET'])
@handle_errors
@validate_player_token
def get_auctions(auth_response=None):
    try:
        response = requests.get(config.dbmanagers.auction + '/auction/status/1')
        response.raise_for_status()
        return make_response(jsonify(market=response.json()), 200)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}, 500))

#POST /api/player/auction/create: Create a new auction listing for a gacha item. (input: gacha id, bid min, auctionStart, auctionEnd etc)
@app.route('/player/auction/create', methods=['POST'])
@handle_errors
@validate_player_token
def create_auction(auth_response=None):
    try:
        data = request.get_json()
        if (not 'gachaCollectionId' in data or
            not 'auctionStart' in data or
            not 'auctionEnd' in data or
            not 'minimumBid' in data) :

            return make_response(jsonify({"message": "Invalid data"}), 400);
    
        tz = pytz.timezone('Europe/Rome')

        try:
            gacha_res = requests.get(f"{config.dbmanagers.gacha}/gachacollection/item/{data["gachaCollectionId"]}")
            gacha_res.raise_for_status()
            if gacha_res.json()['userId'] != auth_response["userId"] :
                return make_response(jsonify({"message": "Invalid user"}), 400);
        except Exception as e:
            return make_response(jsonify({"message": "Gacha Collection does not exits"}), 400);


        start = tz.localize(datetime.strptime(data['auctionStart'], '%Y-%m-%dT%H:%M:%SZ'))
        end = tz.localize(datetime.strptime(data['auctionEnd'], '%Y-%m-%dT%H:%M:%SZ'))
        
        now = datetime.now(tz);
        end = end.replace(second=0, microsecond=0)
        start = start.replace(second=0, microsecond=0)
        now = now.replace(second=0, microsecond=0)

        if (start < now or end < now or start >= end):
            print(start, end, now, flush=True)
            return make_response(jsonify({"message": "Auction start or end time must be in the future"}), 400);
        else :
            print(start, end, now, flush=True)
        # check if user already has an active auction for this gachaCollection
        
        active_auction = requests.get(config.dbmanagers.auction + f'/auction/{auth_response["userId"]}/{data["gachaCollectionId"]}/1')
        try:
            active = active_auction.json()
            print("ACTIVE : ", active, flush=True)
            if(len(active) > 0):
                return make_response(jsonify({"message": f"User {data['userId']} already has an active auction for tha gachaCollection"}), 400);
        except Exception as e:
            print("EXPLODED "+str(e), flush=True)
            print(active, flush=True)
    
        data["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        response = requests.post(config.dbmanagers.auction + '/auction', json=data)
        new_auction = response.json()['auctionId'];
        print(new_auction)

        return make_response(jsonify(auction=response.json()), 201)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)
    
#POST /api/player/auction/{auction_id}/bid: Place a bid on an active auction.
@app.route('/player/auction/bid/<auction_id>', methods=['POST']) ## {userID, amount}
@handle_errors
@validate_player_token
def bid_on_auction(auction_id, auth_response=None):
    try:
        tz = pytz.timezone('Europe/Rome')
        data = request.get_json()
        response = requests.get(config.dbmanagers.auction + f'/auction/{auction_id}')
        response.raise_for_status()
        auction = response.json()

        if (auction["status"] != "ACTIVE" ):
            return make_response(jsonify({"message": "Auction is not active"}), 400);
    
        if (tz.localize(datetime.strptime(auction["auctionStart"], "%a, %d %b %Y %H:%M:%S %Z")).replace(second=0, microsecond=0) > datetime.now(tz).replace(second=0, microsecond=0)):
            return make_response(jsonify({"message": "Auction has not started yet"}), 400);

        if (auction["userId"] == auth_response["userId"]):
            return make_response(jsonify({"message": "Can't bid on an owned auction"}), 400);
    
        if (auction["minimumBid"] > data["bidAmount"]):
            return make_response(jsonify({"message": "Bid amount is lower than minimum bid"}), 400);
        
        auction_bids_resp = requests.get(config.dbmanagers.auction + f'/auctionbid/auction/{auction_id}')
        auction_bids_resp.raise_for_status()
        userBidId = None
        auction_bids = []

        if (auction_bids_resp.status_code == 200):
            auction_bids = auction_bids_resp.json()

        print("auctionBids", auction_bids, flush=True)

        auctionBidAmount = 0

        if len(auction_bids) > 0:
            auction_bids.sort(key=lambda x: x['timestamp'], reverse=True)
            auctionBidAmount = auction_bids[0]['bidAmount']
            userBidId = auction_bids[0]['userId']
        else:
            print("NO BIDS FOR AUCTION " + str(auction_id), flush=True)

        if (userBidId == auth_response["userId"]):
            return make_response(jsonify({"message": "Can't bid twice in a row"}), 400)
        else:
            print("LAST BID USER ID " + str(userBidId), flush=True)
    
        if auctionBidAmount > data["bidAmount"]: 
            return make_response(jsonify({"message": "Bid Amount inferior of previous one"}), 400)
        else:
            print("LAST BID AMOUNT " + str(auctionBidAmount), flush=True)

        bid = {
                'userId': auth_response["userId"],
                'bidCode': f"{auction_id}:{len(auction_bids)}",
                'bidAmount': data["bidAmount"],
                'auctionId':auction_id, 
                'timestamp':datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%SZ")
            }

        try:
            result = requests.post(config.dbmanagers.auction + f'/auctionbid', 
                        json={
                            'userId': auth_response["userId"],
                            'bidCode': f"{auction_id}:{len(auction_bids)}",
                            'bidAmount': data["bidAmount"],
                            'auctionId':auction_id, 
                            'timestamp':datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%SZ")
                        })
            
            result.raise_for_status()
        except Exception as e:
            print("EXPLODED "+str(e), flush=True)
            return make_response(jsonify({"message": str(e)}), 500)
        

        new_bid_id = result.json()['bidId']
        bid["id"] = new_bid_id
        print("BID INSERTED", flush=True)
        
        try:
            ## Subtract money from the current bidder
            resp = requests.patch(
                    f"{config.dbmanagers.user}/user/{auth_response["userId"]}",
                    json={"ingameCurrency": - (float(data['bidAmount']))}
                )
                    
            resp.raise_for_status()

            ## Giving money back to the last bidder
            if userBidId is not None:
                resp1 = requests.patch(f"{config.dbmanagers.user}/user/{userBidId}",
                                    json={"ingameCurrency": float(auctionBidAmount)}
                                )
                
                if resp1.status_code != 200:
                    ## Trying to rollback if the currency isn't changed
                    resp2 = requests.patch(
                        f"{config.dbmanagers.user}/user/{auth_response["userId"]}",
                        json={"ingameCurrency": (float(data['bidAmount']))}
                    )
                    resp1.raise_for_status()
            
        except Exception as e:
            ## Trying to rollback if the currency isn't changed
            response = requests.delete(config.dbmanagers.auction + f'/auctionbid/{new_bid_id}')
            print("BID REMOVED", flush=True)
            return make_response(jsonify({"message": "Unexpected error, retry later"}), 500)

        return make_response(jsonify({"bid": bid}), 200)
    except Exception as err:
        print(str(err), flush=True)
        return make_response(jsonify({"message": str(err)}), 500)

    ## TOKENS DA INSERIRE

@app.route('/player/auction/history', methods=['GET'])
@handle_errors
@validate_player_token
def auction_player_history(auth_response=None):
    try:
        data = request.get_json()
        response = requests.get(config.dbmanagers.auction + f'/auction/{auth_response['userId']}/2')
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
@app.route('/admin/auction', methods=['GET'])
@handle_errors
@validate_admin_token
def get_all_auctions(auth_response=None):
    print(f"GET all auctions")
    try:
        response = requests.get(config.dbmanagers.auction + f'/auction', verify=False)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        auctions = response.json()
        return make_response(jsonify(auctions), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))

    
#GET /auction/<auctions_id>: Admin view specific auction.
@app.route('/admin/auction/<int:auction_id>', methods=['GET'])
@handle_errors
@validate_admin_token
def get_auction(auction_id, auth_response=None):
    print(f"GET auction", auction_id)
    try:
        response = requests.get(config.dbmanagers.auction + f'/auction/{auction_id}', verify=False)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        auction = response.json()
        return make_response(jsonify(auction), 200) ## Substitute with DBManager request,with BIDS
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
    

# PUT /api/admin/auction/{auction_id}: Modify a specific auction.
@app.route('/admin/auction/<int:auction_id>', methods=['PUT'])
@handle_errors
@validate_admin_token
def update_auction(auction_id, auth_response=None):
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
@app.route('/admin/auction/history', methods=['GET'])
@handle_errors
@validate_admin_token
def history(auth_response=None):
    print(f"GET Auctions History")
    try:

        response = requests.get(config.dbmanagers.auction + f'/auction/2')

        response.raise_for_status()

        return make_response(jsonify(response.json()), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
    

@app.route('/admin/auction/history/<user_id>', methods=['GET'])
@handle_errors
@validate_admin_token
def user_history(user_id, auth_response=None):
    print(f"GET History of user " + user_id)
    try:
        data = request.get_json()

        auction = requests.get(config.dbmanagers.auction + f'/auction/user/{user_id}/2')

        return make_response(jsonify(auction.json()), 200) ## Substitute with DBManager request
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))

def create_app():
    return app
