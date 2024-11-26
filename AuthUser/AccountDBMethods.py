from app import app
from app import db
from models import *
from flask import Flask, request, make_response, jsonify

def get_all_accounts():
    accounts = db.session.execute(db.select(Account)).scalars()
    if accounts:
        return jsonify([account.to_dict() for account in accounts])
    return None

def get_single_account(accountId):
    account = db.session.execute(db.select(Account).where(Account.id==accountId)).scalar_one()
    if accounts:
        return jsonify(account.to_dict())
    return None

def get_account_by_username(username):
    account = db.session.execute(db.select(Account).where(Account.username==username)).scalar_one()
    if account:
        return jsonify(account.to_dict())
    return None

def create_account(json_data):
    if json_data:
        account = Account(username=json_data['username'], password=json_data['password'], salt=json_data['salt'])
        db.session.add(account)
        db.session.commit()
        return jsonify({"accountId":account.id})
    return None

def update_account(accountId, json_data):
    if json_data:
        account = get_single_account(accountId)
        if account == None:
            return None
        account.username=json_data['username']
        account.password=json_data['password']
        account.verified = True
        db.session.commit()
        return jsonify({"message":"Account sucessfully updated."})
    return None

def delete_account(accountId):
    account = get_single_account(accountId)
    if account == None:
        return None
    db.session.delete(account)
    db.session.commit()
    return jsonify({"message":"Account sucessfully deleted."})
