from app import app
from app import db
from models import Auction, AuctionStatus
from flask import Flask, request, make_response, jsonify


@app.route('/auction', methods=['GET'])
def get_all_auctions(status):
    auctions = db.session.execute(db.select(Auction)).scalars()
    if auctions:
        return make_response(jsonify([auction.to_dict() for auction in auctions]), 200)
    return make_response(jsonify({"message":"Auctions not found"}), 404)

@app.route('/auction/status/<string:status>', methods=['GET'])
def get_all_auctions_with_status(status):
    auctions = db.session.execute(db.select(Auction).where(Auction.status==status)).scalars()
    if auctions:
        return make_response(jsonify([auction.to_dict() for auction in auctions]), 200)
    return make_response(jsonify({"message":"Auctions not found"}), 404)

@app.route('/auction/<int:auctionId>', methods=['GET'])
def get_single_auction(auctionId):
    auction = db.get_or_404(Auction, auctionId)
    return make_response(jsonify(auction.to_dict()), 200)

@app.route('/auction', methods=['POST'])
def create_auction():
    json_data = request.get_json()
    if json_data:
        auction = Auction(gachaCollectionId=json_data['gachaCollectionId'], userId=json_data["userId"], auctionStart=json_data['auctionStart'], auctionEnd=json_data['auctionEnd'], minimumBid=json_data['minimumBid'], timestamp=json_data['timestamp'],status=json_data['status'])
        db.session.add(auction)
        db.session.commit()
        return make_response(jsonify({"auctionId":auction.id}), 200)
    return make_response(jsonify({"message":"Invalid auction data"}), 400)

@app.route('/auction/<int:auctionId>', methods=['PUT'])
def update_auction(auctionId):
    json_data = request.get_json()
    if json_data:
        auction = db.get_or_404(Auction, auctionId)
        auction.gachaCollectionId=json_data['gachaCollectionId']
        auction.userId=json_data["userId"]
        auction.auctionStart=json_data['auctionStart']
        auction.auctionEnd=json_data['auctionEnd']
        auction.minimumBid=json_data['minimumBid']
        auction.timestamp=json_data['timestamp']
        auction.status=json_data['status']
        auction.verified = True
        db.session.commit()
        return make_response(jsonify({"message":"Auction sucessfully updated."}), 200)
    return make_response(jsonify({"message":"Invalid auction data"}), 400)

@app.route('/auction/user/<int:userId>/<int:status>', methods=['GET'])
def user_auctions(userId, status):
    auctions = db.session.execute(db.select(Auction).where(Auction.status==AuctionStatus(status), Auction.userId==userId)).scalars()
    if auctions:
        return make_response(jsonify([auction.to_dict() for auction in auctions]), 200)
    return make_response(jsonify({"message":"Auctions not found"}), 404)

@app.route('/auction/<int:userId>/<int:collectionId>/<int:status>', methods=['GET'])
def user_gacha_auction(userId, collectionId, status):
    
    auctions = db.session.execute(db.select(Auction).where(Auction.status==AuctionStatus(status), Auction.userId==userId, Auction.gachaCollectionId==collectionId)).scalars()
    if auctions:
        return make_response(jsonify([auction.to_dict() for auction in auctions]), 200)
    return make_response(jsonify({"message":"Auctions not found"}), 404)

@app.route('/auction/<int:auctionId>', methods=['DELETE'])
def delete_auction(auctionId):
    auction = db.get_or_404(Auction, auctionId)
    db.session.delete(auction)
    db.session.commit()
    return make_response(jsonify({"message":"Auction sucessfully deleted."}), 200)
