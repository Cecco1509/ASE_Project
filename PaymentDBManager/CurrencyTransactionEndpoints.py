from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

@app.route('/currencytransaction', methods=['GET'])
def get_all_currency_transactions():
    currencytransactions = db.session.execute(db.select(CurrencyTransaction)).scalars()
    if currencytransactions:
        return make_response(jsonify([currencytransaction.to_dict() for currencytransaction in currencytransactions]), 200)
    return make_response(jsonify({"message":"Currency transactions not found"}), 404)

@app.route('/currencytransaction/<int:userId>', methods=['GET'])
def get_transactions_for_user(userId):
    currencytransactions = db.session.execute(db.select(CurrencyTransaction).where(CurrencyTransaction.userId == userId)).scalars()
    if currencytransactions:
        return make_response(jsonify([currencytransaction.to_dict() for currencytransaction in currencytransactions]), 200)
    return make_response(jsonify({"message":"Currency transactions not found"}), 404)

@app.route('/currencytransaction', methods=['POST'])
def create_currency_transaction():
    json_data = request.get_json()
    if json_data:
        transaction = CurrencyTransaction(userId=json_data['userId'], realAmount=json_data['realAmount'], ingameAmount=json_data['ingameAmount'],timestamp=json_data['timestamp'])
        db.session.add(transaction)
        db.session.commit()
        return make_response(jsonify({"transactionId":transaction.id}), 200)
    return make_response(jsonify({"message":"Invalid currency transaction data"}), 400)

@app.route('/currencytransaction/<int:transactionId>', methods=['DELETE'])
def delete_currency_transaction(transactionId):
    transaction = db.get_or_404(CurrencyTransaction, transactionId)
    db.session.delete(transaction)
    db.session.commit()
    return make_response(jsonify({"messgae":"Transaction sucessfully deleted."}), 200)
