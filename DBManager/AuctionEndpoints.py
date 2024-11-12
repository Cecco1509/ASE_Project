from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

@app.route('/auction/<string:status>', methods=['GET'])
def get_all_auctions_with_status(status):
    auctions = db.session.execute(db.select(Auction).where(Auction.status==status)).scalars()
    if auctions:
        return make_response(jsonify(auctions), 200)
    return make_response(jsonify({"message":"Auctions not found"}), 404)

@app.route('/auction/<int:auctionId>', methods=['GET'])
def get_single_auction(auctionId):
    auction = db.session.execute(db.select(Auction).where(Auction.id==auctionId)).scalar()
    if auction:
        return make_response(jsonify(auction.to_dict()), 200)
    return make_response(jsonify({"message":"Auction not found"}), 404)

@app.route('/auction', methods=['POST'])
def create_auction():
    json_data = request.get_json()
    if json_data:
        auction = Auction(gachaCollectionId=json_data['gachaCollectionId'], auctionStart=json_data['auctionStart'], auctionEnd=json_data['auctionEnd'], minimumBid=json_data['minimumBid'], timestamp=json_data['timestamp'],status=json_data['status'])
        db.session.add(auction)
        db.session.commit()
        return make_response(jsonify(auction.id), 200)
    return make_response(jsonify({"message":"Invalid auction data"}), 400)

@app.route('/auction/<int:auctionId>', methods=['PUT'])
def update_auction(auctionId):
    json_data = request.get_json()
    if json_data:
        auction = db.session.execute(db.select(Auction).where(Auction.id==auctionId)).scalar_one()
        if auction:
            auction.gachaCollectionId=json_data['gachaCollectionId']
            auction.auctionStart=json_data['auctionStart']
            auction.auctionEnd=json_data['auctionEnd']
            auction.minimumBid=json_data['minimumBid']
            auction.timestamp=json_data['timestamp']
            auction.status=json_data['status']
            auction.verified = True
            db.session.commit()
            return make_response(jsonify({"message":"Auction sucessfully updated."}), 200)
        return make_response(jsonify({"message":"Requested auction does not exist"}), 404)
    return make_response(jsonify({"message":"Invalid auction data"}), 400)

@app.route('/auction/<int:auctionId>', methods=['DELETE'])
def delete_auction(auctionId):
    auction = db.session.execute(db.select(Auction).where(Auction.id==auctionId)).scalar_one()
    if auction:
            db.session.delete(auction)
            db.session.commit()
            return make_response(jsonify({"messgae":"Auction sucessfully deleted."}), 200)
    return make_response(jsonify({"message":"Requested auction does not exist"}), 404)