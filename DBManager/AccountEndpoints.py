from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

@app.route('/account', methods=['GET'])
def get_all_accounts():
    accounts = db.session.execute(db.select(Account)).scalars()
    if accounts:
        return make_response(jsonify(accounts), 200)
    return make_response(jsonify({"message":"Accounts not found"}), 404)

@app.route('/account/<int:accountId>', methods=['GET'])
def get_single_aaccount(accountId):
    account = db.session.execute(db.select(Account).where(Account.id==accountId)).scalar()
    if account:
        return make_response(jsonify(account.to_dict()), 200)
    return make_response(jsonify({"message":"Account not found"}), 404)

@app.route('/account', methods=['POST'])
def create_account():
    json_data = request.get_json()
    if json_data:
        account = Account(username=json_data['username'], password=json_data['password'])
        db.session.add(account)
        db.session.commit()
        return make_response(jsonify(account.id), 200)
    return make_response(jsonify({"message":"Invalid account data"}), 400)

@app.route('/account/<int:accountId>', methods=['PUT'])
def update_account(accountId):
    json_data = request.get_json()
    if json_data:
        account = db.session.execute(db.select(Account).where(Account.id==accountId)).scalar_one()
        if account:
            account.username=json_data['username']
            account.password=json_data['password']
            account.verified = True
            db.session.commit()
            return make_response(jsonify({"message":"Account sucessfully updated."}), 200)
        return make_response(jsonify({"message":"Requested account does not exist"}), 404)
    return make_response(jsonify({"message":"Invalid account data"}), 400)

@app.route('/account/<int:accountId>', methods=['DELETE'])
def delete_account(acoountId):
    account = db.session.execute(db.select(Account).where(Account.id==accountId)).scalar_one()
    if account:
            db.session.delete(account)
            db.session.commit()
            return make_response(jsonify({"messgae":"Account sucessfully deleted."}), 200)
    return make_response(jsonify({"message":"Requested account does not exist"}), 404)
