from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

@app.route('/auctiontransaction', methods=['GET'])
def get_all_auction_transactions():
    transactions = db.session.execute(db.select(AuctionTransaction)).scalars()
    if transactions:
        return make_response(jsonify([transaction.to_dict() for transaction in transactions]), 200)
    return make_response(jsonify({"message":"Auction transactions not found"}), 404)

@app.route('/auctiontransaction/<int:transactionId>', methods=['GET'])
def get_single_auctiontransaction(transactionId):
    transaction = db.get_or_404(AuctionTransaction, transactionId)
    return make_response(jsonify(transaction.to_dict()), 200)

@app.route('/auctiontransaction/user/<int:userId>', methods=['GET'])
def get_auctiontransactions_for_user(userId):
    transactions = db.session.execute(db.select(AuctionTransaction).where(AuctionTransaction.sellerId==userId or AuctionTransaction.buyerId==userId)).scalars()
    if transactions:
        return make_response(jsonify([transaction.to_dict() for transaction in transactions]), 200)
    return make_response(jsonify({"message":"Auction transactions not found"}), 404)

@app.route('/auctiontransaction', methods=['POST'])
def create_transaction():
    json_data = request.get_json()
    if json_data:
        transaction = AuctionTransaction(sellerId=json_data['sellerId'], buyerId=json_data['buyerId'], auctionBidId=json_data['auctionBidId'], timestamp=json_data['timestamp'])
        db.session.add(transaction)
        db.session.commit()
        return make_response(jsonify({"transactionId":transaction.id}), 200)
    return make_response(jsonify({"message":"Invalid auction transaction data"}), 400)

@app.route('/auctiontransaction/<int:transactionId>', methods=['PUT'])
def update_transaction(transactionId):
    json_data = request.get_json()
    if json_data:
        transaction = db.get_or_404(AuctionTransaction, transactionId)
        transaction.sellerId=json_data['sellerId']
        transaction.buyerId=json_data['buyerId']
        transaction.auctionBidId=json_data['auctionBidId']
        transaction.timestamp=json_data['timestamp']
        transaction.verified = True
        db.session.commit()
        return make_response(jsonify({"message":"Transaction sucessfully updated."}), 200)
    return make_response(jsonify({"message":"Invalid transaction data"}), 400)

@app.route('/transaction/<int:transactionId>', methods=['DELETE'])
def delete_transaction(transactionId):
    transaction = db.get_or_404(AuctionTransaction, transactionId)
    db.session.delete(transaction)
    db.session.commit()
    return make_response(jsonify({"message":"Transaction sucessfully deleted."}), 200)
