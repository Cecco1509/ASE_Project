from datetime import datetime
import requests
from flask import jsonify

from flask import Flask, request, make_response, jsonify
from auth_utils import *
from handle_errors import *
from auction_mock_db import *

app = Flask(__name__, instance_relative_config=True)

############################################################# USER ##########################################################

@app.route('/api/player/auction/market', methods=['GET'])
@handle_errors
def get_auctions():
    try:
        return make_response(jsonify([auction for auction in mock_auctions if auction['status'] == "ACTIVE"]), 200)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}, 500))

#POST /api/player/auction/create: Create a new auction listing for a gacha item. (input: gacha id, bid min, auctionStart, auctionEnd etc)
@app.route('/api/player/auction/create', methods=['POST'])
@handle_errors
def create_auction():
    try:
        data = request.get_json()
        if (not 'gachaCollectionId' in data or
            not 'auctionStart' in data or
            not 'auctionEnd' in data or
            not 'minimumBid' in data) :

            return make_response(jsonify({"message": "Invalid data"}), 400)
        
        ok = False
        for gacha_collection in mock_gacha_collection_list:
            if gacha_collection["userId"] == data["userId"] and gacha_collection["gachaId"] == data["gachaCollectionId"]:
                ok = True
                break

        if not ok:
            return make_response(jsonify({"message": "User does not have the required gacha collection"}), 400)

        start = datetime.strptime(data['auctionStart'], '%Y-%m-%dT%H:%M:%S.%fZ')
        end = datetime.strptime(data['auctionEnd'], '%Y-%m-%dT%H:%M:%S.%fZ')
        
        now = datetime.now();
        end = end.replace(second=0, microsecond=0)
        cmp_now = now.replace(second=0, microsecond=0)

        if (start < cmp_now):
            return make_response(jsonify({"message": "Auction start time must be in the future"}), 400);
    
        if end < cmp_now:
            return make_response(jsonify({"message": "Auction end time must be in the future"}), 400);
    
        if (start >= end):
            return make_response(jsonify({"message": "Auction start time must be before end time"}), 400);

        # check if user already has an active auction for this gachaCollection
        ok = True
        for auction in mock_auctions:
            if auction["status"] == "ACTIVE" and auction["gachaCollectionId"] == data["gachaCollectionId"]:
                ok = False
                break

        if not ok:
            return make_response(jsonify({"message": "User already has an active auction for this gacha collection"}), 400);
    
        data["timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        new_auction = {
            "id": len(mock_auctions) + 1,
            "gachaCollectionId": data["gachaCollectionId"],
            "userId": data["userId"],
            "auctionStart": start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "auctionEnd": end.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "minimumBid": data["minimumBid"],
            "timestamp": data["timestamp"],
            "status": "ACTIVE"
        }

        mock_auctions.append(new_auction)

        return make_response(jsonify({"auctionId" : new_auction["id"]}), 201)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)
    
#POST /api/player/auction/{auction_id}/bid: Place a bid on an active auction.
@app.route('/api/player/auction/bid/<int:auction_id>', methods=['POST']) ## {userID, amount}
@handle_errors
def bid_on_auction(auction_id):
    try:
        data = request.get_json()

        if ("bidAmount" not in data or
            "userId" not in data ):
            return make_response(jsonify({"message": "invalid payload"}), 400);

        auction = None
        for auction_data in mock_auctions:
            if auction_data["id"] == auction_id:
                auction = auction_data
                break

        if auction is None:
            return make_response(jsonify({"message": "Auction not found"}), 404);

        if (auction["status"] != "ACTIVE" ):
            return make_response(jsonify({"message": "Auction is not active"}), 400);
    
        if auction["auctionStart"] > datetime.now():
            return make_response(jsonify({"message": "Auction has not started yet"}), 400);

        if (auction["userId"] == data["userId"]):
            return make_response(jsonify({"message": "Can't bid on an owned auction"}), 400);
    
        if (auction["minimumBid"] > data["bidAmount"]):
            return make_response(jsonify({"message": "Bid amount is lower than minimum bid"}), 400);

        auction_bids = []
        for bid in mock_auction_bids:
            if bid['auctionId'] == auction_id:
                auction_bids.append(bid)

        userBidId = None
        auctionBidAmount = 0

        if len(auction_bids) > 0:
            auction_bids.sort(key=lambda x: x['timestamp'], reverse=True)
            auctionBidAmount = auction_bids[0]['bidAmount']
            userBidId = auction_bids[0]['userId']
        else:
            print("NO BIDS FOR AUCTION " + str(auction_id), flush=True)

        if (userBidId == data["userId"]):
            return make_response(jsonify({"message": "Can't bid twice in a row"}), 400)
        else:
            print("LAST BID USER ID " + str(userBidId), flush=True)
    
        if auctionBidAmount > data["bidAmount"]: 
            return make_response(jsonify({"message": "Bid Amount inferior of previous one"}), 400)
        else:
            print("LAST BID AMOUNT " + str(auctionBidAmount), flush=True)

        bid = {
                'id': len(mock_auction_bids) + 1,
                'userId': data["userId"],
                'bidAmount': data["bidAmount"],
                'auctionId': auction_id, 
                'timestamp': datetime.now()
            }

        mock_auction_bids.append(bid)

        # update users ingameCurrency

        return make_response(jsonify({"bidId": bid["id"]}), 200)
    except Exception as err:
        print(str(err), flush=True)
        return make_response(jsonify({"message": str(err)}), 500)

@app.route('/api/player/auction/history', methods=['GET'])
@handle_errors
def auction_player_history():
    try:
        return make_response(jsonify([auction for auction in mock_auctions if auction['status'] == "PASSED"
                                                                            and auction["userId"] == 2]), 200)
    except Exception as err:
        return make_response(jsonify({"message": str(err)}), 500)

##################################################### ADMIN ############################################################

#GET /auctions: Admin view of all auctions.
@app.route('/api/admin/auction', methods=['GET'])
@handle_errors
def get_all_auctions():
    print(f"GET all auctions")
    try:
        return make_response(jsonify(mock_auctions), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))

    
#GET /auction/<auctions_id>: Admin view specific auction.
@app.route('/api/admin/auction/<int:auction_id>', methods=['GET'])
@handle_errors
def get_auction(auction_id):
    print(f"GET auction", auction_id)
    try:
        auction = None
        for auction_data in mock_auctions:
            if auction_data["id"] == auction_id:
                auction = auction_data
                break

        if auction is None:
            return make_response(jsonify({"message": "Auction not found"}), 404)
        return make_response(jsonify(auction), 200) ## Substitute with DBManager request,with BIDS
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
    

# PUT //api/admin/auction/{auction_id}: Modify a specific auction.
@app.route('/api/admin/auction/<int:auction_id>', methods=['PUT'])
@handle_errors
def update_auction(auction_id):
    print(f"PUT auction ", auction_id, flush=True) 
    try:
        # Parse JSON data from the request
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({"message": "Invalid auction data"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": "Invalid JSON data"}), 400)
        
        # Validate auction data
        if (
            not 'auctionStart' in data or
            not 'auctionEnd' in data or
            not 'status' in data) :

            return make_response(jsonify({"message": "Invalid data"}), 400);
        
        auction = None
        for auction_data in mock_auctions:
            if auction_data["id"] == auction_id:
                auction = auction_data
                break
        
        if auction is None:
            return make_response(jsonify({"message": "Auction not found"}), 404)
        
        if data["auctionStart"] is not None:
            start = datetime.strptime(data['auctionStart'], '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            start = None
        
        if data["auctionEnd"] is not None:
            end = datetime.strptime(data['auctionEnd'], '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            end = None
        
        now = datetime.now()
        if end is not None:
            end = end.replace(second=0, microsecond=0)
        cmp_now = now.replace(second=0, microsecond=0)
        
        if (start is not None and auction["auctionStart"] < cmp_now):
            return make_response(jsonify({"message": "Auction is already started, cannot modify its start time"}), 400);
    
        if (start is not None and start < cmp_now):
            return make_response(jsonify({"message": "Auction start time must be in the future"}), 400);
    
        if end is not None and end < cmp_now:
            return make_response(jsonify({"message": "Auction end time must be in the future"}), 400);
    
        if (start is not None and end is not None and start >= end):
            return make_response(jsonify({"message": "Auction start time must be before end time"}), 400);
    
        if (data["status"] is not None and data["status"] == "ACTIVE"):
            if auction["auctionEnd"] <= cmp_now:
                return make_response(jsonify({"message": "Auction cannot be started after it has already ended"}), 400);

        if data["status"] == "PASSED" and auction["status"] != "PASSED" and data["auctionEnd"] is None and data["auctionStart"] is None:
            #close_auction(auction)
            auction["status"] = "PASSED"
            auction["auctionEnd"] = now
            print("CLOSED", flush=True)
        elif data["status"] == "PASSED" and data["auctionEnd"] is None and data["auctionStart"] is None:
            return make_response(jsonify({"message": "Auction cannot be ended twice"}), 400);
        elif data["status"] == "PASSED":
            return make_response(jsonify({"message": "Cannot set start time or end time when closing an auction"}), 400);

        if data["status"] != "PASSED":
            if (data["status"] is not None):
                auction["status"] = data["status"]
            if (data["auctionEnd"] is not None):
                auction["auctionEnd"] = datetime.strptime(data["auctionEnd"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if (data["auctionStart"] is not None):
                auction["auctionStart"] = datetime.strptime(data["auctionStart"], "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Return success response
        return make_response(jsonify(auction), 200)
    except requests.exceptions.RequestException as e:
        print(f"External request failed: {e}")
        return make_response(jsonify({"message": "Failed to update auction", "error": str(e)}), 500)

    
# GET /api/admin/auction/history: Admin view of all market history (old auctions).
@app.route('/api/admin/auction/history', methods=['GET'])
@handle_errors
def history():
    print(f"GET Auctions History")
    try:
        return make_response(jsonify([auction for auction in mock_auctions if auction['status'] == "PASSED"]), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
    

@app.route('/api/admin/auction/history/<int:user_id>', methods=['GET'])
@handle_errors
def user_history(user_id):
    print(f"GET History of user " + str(user_id))
    try:
        return make_response(jsonify([auction for auction in mock_auctions if auction['status'] == "PASSED"
                                                                            and auction["userId"] == user_id]), 200)
    except Exception as e:
        return make_response(jsonify({"message": str(e)}, 500))
    


## Mock auth

@app.route('/api/admin/login', methods=['POST'])
def login_admin():
    return make_response(jsonify({"Access token" : ""}), 200)

@app.route('/api/player/login', methods=['POST'])
def login_player():
    return make_response(jsonify({"Access token" : ""}), 200)

def create_app():
    return app
