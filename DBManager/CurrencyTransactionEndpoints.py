from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify
from enums import UserStatus

@app.route('/currencytransaction', methods=['GET'])
def get_all_currency_transactions():
    currencytransactions = db.session.execute(db.select(CurrencyTransaction)).scalars()
    if currencytransactions:
        return make_response(jsonify(currencytransactions), 200)
    return make_response(jsonify({"message":"Currency transactions not found"}), 404)

@app.route('/currencytransaction/<int:userId>', methods=['GET'])
def get_transactions_for_user(userId):
    currencytransaction = db.session.execute(db.select(CurrencyTransaction).where(CurrencyTransaction.userId == userId)).scalar()
    if currencytransaction:
        return make_response(jsonify(currencytransaction.to_dict()), 200)
    return make_response(jsonify({"message":"Currency transactions not found"}), 404)

@app.route('/currencytransaction', methods=['POST'])
def create_currency_transaction():
    json_data = request.get_json()
    if json_data:
        transaction = CurrencyTransaction(userId=json_data['userId'], realMount=json_data['realMount'], ingameMount=json_data['ingameMount'],timestamp=json_data['timestamp'])
        db.session.add(transaction)
        db.session.commit()
        return make_response(jsonify(transaction.id), 200)
    return make_response(jsonify({"message":"Invalid currency transaction data"}), 400)

@app.route('/currencytransaction/<int:transactionId>', methods=['DELETE'])
def delete_currency_transaction(transactionId):
    transaction = db.session.execute(db.select(CurrencyTransaction).where(CurrencyTransaction.id==transactionId)).scalar_one()
    if transaction:
            db.session.delete(transaction)
            db.session.commit()
            return make_response(jsonify({"messgae":"Transaction sucessfully deleted."}), 200)
    return make_response(jsonify({"message":"Requested transaction does not exist"}), 404)