from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

@app.route('/auctionbid', methods=['GET'])
def get_all_auction_bids():
    bids = db.session.execute(db.select(AuctionBid)).scalars()
    if bids:
        return make_response(jsonify(bids), 200)
    return make_response(jsonify({"message":"Auction bids not found"}), 404)

@app.route('/auctionbid/<int:bidId>', methods=['GET'])
def get_single_auctiontbid(bidId):
    bid = db.session.execute(db.select(AuctionBid).where(AuctionBid.id==bidId)).scalar()
    if bid:
        return make_response(jsonify(bid.to_dict()), 200)
    return make_response(jsonify({"message":"Auction bid not found"}), 404)

@app.route('/auctionbid/user/<int:userId>', methods=['GET'])
def get_auctionbids_for_user(userId):
    bid = db.session.execute(db.select(AuctionBid).where(AuctionBid.userId==userId)).scalar()
    if bid:
        return make_response(jsonify(bid.to_dict()), 200)
    return make_response(jsonify({"message":"Auction bids not found"}), 404)

@app.route('/auctionbid', methods=['POST'])
def create_auctionbid():
    json_data = request.get_json()
    if json_data:
        bid = AuctionBid(userId=json_data['userId'], bidAmount=json_data['bidAmount'], auctionId=json_data['auctionId'], timestamp=json_data['timestamp'])
        db.session.add(bid)
        db.session.commit()
        return make_response(jsonify(bid.id), 200)
    return make_response(jsonify({"message":"Invalid auction bid data"}), 400)

@app.route('/auctionbid/<int:bidId>', methods=['PUT'])
def update_bid(bidId):
    json_data = request.get_json()
    if json_data:
        bid = db.session.execute(db.select(AuctionBid).where(AuctionBid.id==bidId)).scalar_one()
        if bid:
            bid.userId=json_data.userId
            bid.bidAmount=json_data.bidAmount
            bid.auctionId=json_data.auctionId
            bid.timestamp=json_data.timestamp
            bid.verified = True
            db.session.commit()
            return make_response(jsonify({"message":"Auction bid sucessfully updated."}), 200)
        return make_response(jsonify({"message":"Requested auction bid does not exist"}), 404)
    return make_response(jsonify({"message":"Invalid auction bid data"}), 400)

@app.route('/auctionbid/<int:bidId>', methods=['DELETE'])
def delete_bid(bidId):
    bid = db.session.execute(db.select(AuctionBid).where(AuctionBid.id==bidId)).scalar_one()
    if bid:
            db.session.delete(bid)
            db.session.commit()
            return make_response(jsonify({"messgae":"Auction bid sucessfully deleted."}), 200)
    return make_response(jsonify({"message":"Requested auction bid does not exist"}), 404)
